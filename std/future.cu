#include <iostream>
#include <thread>
// #include <functional>
#include <future>
#include <algorithm>
#include <vector>
#include <cuda.h>

__global__ void NoOpKernel() {}

using namespace std;

float ThreadFn(cudaEvent_t start_evt, vector<cudaEvent_t>& evts) {
  float ms = 0.0, ret = -1.0;
  for (auto evt : evts) {
    cudaEventSynchronize(evt);
    cudaEventElapsedTime(&ms, start_evt, evt);
    ret = max(ret, ms);
    cout << ms << endl;
  }

  return ret;
}

int main() {
  cudaStream_t stream;
  cudaStreamCreate(&stream);

  vector<cudaEvent_t> evts;

  cudaEvent_t start_evt;
  cudaEventCreate(&start_evt);
  cudaEventRecord(start_evt);

  for (int i = 0; i < 20; i++) {
    NoOpKernel<<<1, 128, 0, stream>>>();
    cudaEvent_t evt;
    cudaEventCreate(&evt);
    cudaEventRecord(evt, stream);
    evts.push_back(evt);
  }

  // std::future<float> val_future
  auto val_future = async(launch::async, ThreadFn, start_evt, ref(evts));
  cout << val_future.get() << endl;

  return 0;
}