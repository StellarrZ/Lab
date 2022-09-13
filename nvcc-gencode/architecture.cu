#include <cuda.h>
#include <cuda_runtime.h>
#include <cstdio>


int main() {
  cudaDeviceProp prop;
  cudaGetDeviceProperties(&prop, 0);
  if (cudaGetLastError() != cudaSuccess) {
    fprintf(stderr, "Failed to get CUDA device #0.\n");
    printf(" ");
  } else {
    int generation = prop.major * 10 + prop.minor;
    printf("NVCC_GENCODE=\"-gencode arch=compute_%d,code=sm_%d\"", generation, generation);
  }

  return 0;
}