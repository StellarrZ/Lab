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

__global__ void noOp() {}


int main() {
  cudaStream_t stream;
  cudaStreamCreate(&stream);

  cudaEvent_t start_evt_1, end_evt_1;
  cudaEvent_t start_evt_2, end_evt_2;
  cudaEventCreate(&start_evt_1);
  cudaEventCreate(&end_evt_1);
  cudaEventCreate(&start_evt_2);
  cudaEventCreate(&end_evt_2);

  float ms_1, ms_2;

  for (int i = 0; i < 100; i++) {
    // cudaEventRecord(start_evt_1, stream);
    // cuSleep<<<1, 32, 0, stream>>>();
    // cuSleep<<<1, 32, 0, stream>>>();
    // cuSleep<<<1, 32, 0, stream>>>();
    // cuSleep<<<1, 32, 0, stream>>>();
    // cuSleep<<<1, 32, 0, stream>>>();
    // cudaEventRecord(end_evt_1, stream);

    // cudaEventRecord(start_evt_2, stream);
    // cuSleep<<<1, 32, 0, stream>>>();
    // cuSleep<<<1, 32, 0, stream>>>();
    // cuSleep<<<1, 32, 0, stream>>>();
    // cuSleep<<<1, 32, 0, stream>>>();
    // cuSleep<<<1, 32, 0, stream>>>();
    // cudaEventRecord(end_evt_2, stream);

    cudaEventRecord(start_evt_2, stream);
    noOp<<<1, 32, 0, stream>>>();
    noOp<<<1, 32, 0, stream>>>();
    noOp<<<1, 32, 0, stream>>>();
    noOp<<<1, 32, 0, stream>>>();
    noOp<<<1, 32, 0, stream>>>();
    cudaEventRecord(end_evt_2, stream);

    cudaEventRecord(start_evt_1, stream);
    cuSleep<<<1, 32, 0, stream>>>();
    cuSleep<<<1, 32, 0, stream>>>();
    cuSleep<<<1, 32, 0, stream>>>();
    cuSleep<<<1, 32, 0, stream>>>();
    cuSleep<<<1, 32, 0, stream>>>();
    cudaEventRecord(end_evt_1, stream);

    // std::this_thread::sleep_for(std::chrono::milliseconds(200));  // 200 ms

    cudaEventSynchronize(end_evt_1);
    cudaEventElapsedTime(&ms_1, start_evt_1, end_evt_1);

    cudaEventSynchronize(end_evt_2);
    cudaEventElapsedTime(&ms_2, start_evt_2, end_evt_2);

    printf("%f ms  %f ms\n", ms_1, ms_2);
  }


  return 0;
}