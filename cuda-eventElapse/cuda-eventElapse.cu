#include <cuda.h>
#include <cuda_runtime.h>
#include <thread>
#include <chrono>
#include <cstdio>

__global__ void cuSleep() {
  for (int i = 0; i < 10; i++) {  // 10 ms
    __nanosleep(1000000U);  // 1 ms
  }
}


int main() {
  cudaStream_t stream;
  cudaStreamCreate(&stream);

  cudaEvent_t start_evt, end_evt;
  cudaEventCreate(&start_evt);
  cudaEventCreate(&end_evt);

  float ms;

  for (int i = 0; i < 100; i++) {
    cudaEventRecord(start_evt, stream);
    cuSleep<<<1, 32, 0, stream>>>();
    cudaEventRecord(end_evt, stream);

    std::this_thread::sleep_for(std::chrono::milliseconds(200)); // 200 ms

    cudaEventSynchronize(end_evt);
    cudaEventElapsedTime(&ms, start_evt, end_evt);

    printf("%f ms\n", ms);
  }


  return 0;
}