#include <cstdio>
#include <cuda_runtime.h>


int main() {
  int num_gpu;
  cudaGetDeviceCount(&num_gpu);

  cudaDeviceProp property;

  for (int i = 0; i < num_gpu; i++) {
    cudaGetDeviceProperties(&property, i);
    printf("%ld  %ld  %ld\n", 
            property.textureAlignment, 
            property.texturePitchAlignment, 
            property.surfaceAlignment);
  }
  return 0;
}