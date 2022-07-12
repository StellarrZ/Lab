#include <iostream>
#include <vector>
#include <mutex>
#include <condition_variable>

#include "cuda_runtime.h"

#include <cstdio>
#include <cstdlib>

#define CUDACHECK(cmd) do {                         \
  cudaError_t e = cmd;                              \
  if( e != cudaSuccess ) {                          \
    printf("Failed: Cuda error %s:%d '%s'\n",       \
        __FILE__,__LINE__,cudaGetErrorString(e));   \
    exit(EXIT_FAILURE);                             \
  }                                                 \
} while(0)


// empty kernel
__global__ void NoOpKernel() {}


// for blocking stream to wait for host signal
class Event {
 private:
  std::mutex mtx_condition_;
  std::condition_variable condition_;
  bool signalled = false;

 public:
  void Signal() {
    {
      std::lock_guard<decltype(mtx_condition_)> lock(mtx_condition_);
      signalled = true;
    }
    condition_.notify_all();
  }

  void Wait() {
    std::unique_lock<decltype(mtx_condition_)> lock(mtx_condition_);
    while (!signalled) {
      condition_.wait(lock);
    }
  }
};

void CUDART_CB block_op_host_fn(void* arg) {
  Event* evt = (Event*)arg;
  evt->Wait();
}


static cudaEvent_t end_event;

int main() {
  cudaStream_t stream1, stream2;
  CUDACHECK(cudaStreamCreate(&stream1));
  CUDACHECK(cudaStreamCreate(&stream2));

  int num_events = 150; // hangs if THIS >= 57
  std::vector<std::shared_ptr<Event>> event_vec;

  for (int i = 0; i < num_events; i++) {
    NoOpKernel<<<1, 128, 0, stream1>>>();

    event_vec.push_back(std::make_shared<Event>());
    cudaLaunchHostFunc(stream1, block_op_host_fn, event_vec.back().get());

    std::cout << "Before recording #" << i << std::endl;
    CUDACHECK(cudaEventCreate(&end_event));
    CUDACHECK(cudaEventRecord(end_event, stream1));
    // CUDACHECK(cudaEventRecord(end_event, stream2));
    std::cout << "After recording  #" << i << std::endl;

    // NoOpKernel<<<1, 128, 0, stream1>>>();
  }

  for (int i = 0; i < num_events; i++) {
    event_vec[i]->Signal();
  }

  // clean up
  CUDACHECK(cudaDeviceSynchronize());
  CUDACHECK(cudaEventDestroy(end_event));
  CUDACHECK(cudaStreamDestroy(stream1));
  CUDACHECK(cudaStreamDestroy(stream2));
  return 0;
}