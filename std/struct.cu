#include <iostream>
#include <thread>
// #include <functional>
#include <future>
#include <algorithm>
#include <vector>
#include <cuda.h>

__global__ void NoOpKernel() {}

using namespace std;

typedef struct packedData {
  __uint128_t data_amount;
  cudaEvent_t start_evt;
  std::vector<cudaEvent_t> end_evts;
} PackedData;

class C {
public:
  bool b_dumb;
  PackedData data;

  C(): b_dumb(true),
       data({0, nullptr, vector<cudaEvent_t>()}) {}
};

float ThreadFn(PackedData* data_ptr) {
  float ms = 0.0, ret = -1.0;
  for (auto evt : data_ptr->end_evts) {
    cudaEventSynchronize(evt);
    cudaEventElapsedTime(&ms, data_ptr->start_evt, evt);
    ret = max(ret, ms);
    cout << ms << endl;
  }

  return ret;
}

int main() {
  cudaStream_t stream;
  cudaStreamCreate(&stream);

  C c;

  cudaEventCreate(&c.data.start_evt);
  cudaEventRecord(c.data.start_evt);

  for (int i = 0; i < 20; i++) {
    NoOpKernel<<<1, 128, 0, stream>>>();
    cudaEvent_t evt;
    cudaEventCreate(&evt);
    cudaEventRecord(evt, stream);
    c.data.end_evts.push_back(evt);
  }

  // std::future<float> val_future
  auto val_future = async(launch::async, ThreadFn, &c.data);
  cout << val_future.get() << endl;

  return 0;
}