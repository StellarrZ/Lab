#include <iostream>
#include <chrono>
#include <cuda.h>
#include <cuda_runtime.h>

int main() {
  cudaSetDevice(0);
  float* host = (float*)malloc(32);
  float* device;
  cudaMalloc(&device, 32);
  
  cudaEvent_t sta, end;
  cudaEventCreate(&sta);
  cudaEventCreate(&end);

  for (int i = 0; i < 100; i++) {
    // cudaEventRecord(sta);
    auto begin = std::chrono::steady_clock::now();
    cudaMemcpy(device, host, 32, cudaMemcpyHostToDevice);
    auto final = std::chrono::steady_clock::now();
    // cudaEventRecord(end);

    // float ms;
    // cudaEventSynchronize(end);
    // cudaEventElapsedTime(&ms, sta, end);

    std::cout << (float)std::chrono::duration_cast<std::chrono::nanoseconds>(final - begin).count() / 1E6 << std::endl;
    // std::cout << ms << "  " << (float)std::chrono::duration_cast<std::chrono::nanoseconds>(final - begin).count() / 1E6 << std::endl;
  }

  return 0;
}