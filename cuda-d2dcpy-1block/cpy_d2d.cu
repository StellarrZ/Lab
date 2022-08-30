#include <iostream>
#include <cuda_runtime.h>


#define CUDACHECK(cmd) do {                         \
  cudaError_t e = cmd;                              \
  if( e != cudaSuccess ) {                          \
    printf("Failed: Cuda error %s:%d '%s'\n",       \
        __FILE__,__LINE__,cudaGetErrorString(e));   \
    exit(EXIT_FAILURE);                             \
  }                                                 \
} while(0)


/* Kernel 1 - Bad data locality */
__global__ void memcpyD2D_a(float* src, float* dst, int num_elem) {
  int tid = blockIdx.x * blockDim.x + threadIdx.x;  // 0 + threadIdx.x
  int stride = blockDim.x * gridDim.x;  // blockDim.x * 1
  int tile = num_elem / stride;

  for (int k = 0; k < tile; k++) {
    dst[k + tid * tile] = src[k + tid * tile];
  }
}

/* Kernel 2 - Okay data locality */
__global__ void memcpyD2D_b(float* src, float* dst, int num_elem) {
  int tid = blockIdx.x * blockDim.x + threadIdx.x;  // 0 + threadIdx.x
  int stride = blockDim.x * gridDim.x;  // blockDim.x * 1

  for (int k = 0; k < num_elem; k += stride) {
    dst[k + tid] = src[k + tid];
  }
}

#define FETCH_FLOAT4(pointer) (reinterpret_cast<float4*>(&(pointer))[0])
/* Kernel 3 - Vectorized mem access */
__global__ void memcpyD2D_c(float* src, float* dst, int num_elem) {
  int tid = (blockIdx.x * blockDim.x + threadIdx.x) * 4;  // (0 + threadIdx.x) * 4
  int stride = blockDim.x * gridDim.x * 4;  // blockDim.x * 1 * 4

  for (int k = 0; k < num_elem; k += stride) {
    float4 src4 = FETCH_FLOAT4(src[k + tid]);
    FETCH_FLOAT4(dst[k + tid]) = src4;
  }
}


int main(int argc, char* argv[]) {
  CUDACHECK(cudaSetDevice(0));

  cudaStream_t stream;
  CUDACHECK(cudaStreamCreate(&stream));

  const size_t num_of_bytes = 4 << 20;
  float* h_buf;
  float* d_src;
  float* d_dst;

  h_buf = (float*)malloc(num_of_bytes);
  CUDACHECK(cudaMalloc(&d_src, num_of_bytes));
  CUDACHECK(cudaMalloc(&d_dst, num_of_bytes));

  int num_elem = num_of_bytes / sizeof(float);

  for (int i = 0; i < num_elem; i++) {
    // h_buf[i] = static_cast<float>(rand()) / static_cast<float>(RAND_MAX);
    h_buf[i] = 1.0;
  }
  CUDACHECK(cudaMemcpy(d_src, h_buf, num_of_bytes, cudaMemcpyHostToDevice));

  cudaEvent_t start, stop;
  CUDACHECK(cudaEventCreate(&start));
  CUDACHECK(cudaEventCreate(&stop));

  for (int j = 0; j < 100; j++) {
    CUDACHECK(cudaEventRecord(start, stream));
    // memcpyD2D_a<<<1, 1024, 0, stream>>>(d_src, d_dst, num_elem);
    // memcpyD2D_b<<<1, 1024, 0, stream>>>(d_src, d_dst, num_elem);
    memcpyD2D_c<<<1, 1024, 0, stream>>>(d_src, d_dst, num_elem);
    CUDACHECK(cudaEventRecord(stop, stream));

    // if (cudaGetLastError() != cudaSuccess) {
    //   std::cout << "Got ERROR" << std::endl;
    // }

    CUDACHECK(cudaEventSynchronize(stop));
    float milliseconds = 0;
    CUDACHECK(cudaEventElapsedTime(&milliseconds, start, stop));

    std::cout<< "Took time(ms) : " << milliseconds << std::endl;

    CUDACHECK(cudaStreamSynchronize(stream));
  }


  size_t cnt = 0;
  float* check = (float*)malloc(num_of_bytes);
  CUDACHECK(cudaMemcpy(check, d_dst, num_of_bytes, cudaMemcpyDeviceToHost));
  for (int i = 0; i < num_elem; i++) {
    if (check[i] < 0.9 || check[i] > 1.1) {
      cnt++;
      // printf("Not match: %d  %f\n", i, check[i]);
    }
  }
  std::cout << cnt << std::endl;
}