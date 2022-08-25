#include<cstdio>
#include<iostream>
#include<cuda_runtime.h>
#include<chrono>


int main() {
  cudaSetDevice(0);

  size_t num_bytes = 25 << 20;
  float *src, *dst;
  cudaMalloc(&src, num_bytes);
  cudaMalloc(&dst, num_bytes);

  for (int i = 0; i < 100; i++) {
    auto start = std::chrono::system_clock::now();
    cudaMemcpy(dst, src, num_bytes, cudaMemcpyDeviceToDevice);
    auto end = std::chrono::system_clock::now();
    std::cout << std::chrono::duration_cast<std::chrono::nanoseconds>(
                    end.time_since_epoch() - start.time_since_epoch()).count()
              << " ns" 
              << std::endl;
  }
}