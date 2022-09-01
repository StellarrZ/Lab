#include <cstdio>
#include <cuda.h>
#include <cuda_runtime.h>
#include <cooperative_groups/memcpy_async.h>
#include <cuda/pipeline>


__device__ void compute(int* global_out, int const* shared_in) {

}

__global__ void with_staging(int* global_out, int const* global_in, size_t size, size_t batch_sz) {
    auto grid = cooperative_groups::this_grid();
    auto block = cooperative_groups::this_thread_block();

    // printf("%lld  %d  %d  %d  %d\n", grid.size(), block.size(), blockIdx.x, blockDim.x, threadIdx.x);
    // printf("%d\n", block.group_index().x);
    assert(size == batch_sz * grid.size()); // Assume input size fits batch_sz * grid_size

    constexpr size_t stages_count = 2; // Pipeline with two stages
    // Two batches must fit in shared memory:
    extern __shared__ int shared[];  // stages_count * block.size() * sizeof(int) bytes
    size_t shared_offset[stages_count] = { 0, block.size() }; // Offsets to each batch

    // Allocate shared storage for a two-stage cuda::pipeline:
    __shared__ cuda::pipeline_shared_state<
        cuda::thread_scope::thread_scope_block,
        stages_count
    > shared_state;
    auto pipeline = cuda::make_pipeline(block, &shared_state);

    // Each thread processes `batch_sz` elements.
    // Compute offset of the batch `batch` of this thread block in global memory:
    auto block_batch = [&](size_t batch) -> int {
      return block.group_index().x * block.size() + grid.size() * batch;
    };

    // Initialize first pipeline stage by submitting a `memcpy_async` to fetch a whole batch for the block:
    if (batch_sz == 0) return;
    pipeline.producer_acquire();
    cuda::memcpy_async(block, shared + shared_offset[0], global_in + block_batch(0), sizeof(int) * block.size(), pipeline);
    pipeline.producer_commit();

    // Pipelined copy/compute:
    for (size_t batch = 1; batch < batch_sz; ++batch) {
        // Stage indices for the compute and copy stages:
        size_t compute_stage_idx = (batch - 1) % 2;
        size_t copy_stage_idx = batch % 2;

        size_t global_idx = block_batch(batch);

        // Collectively acquire the pipeline head stage from all producer threads:
        pipeline.producer_acquire();

        // Submit async copies to the pipeline's head stage to be
        // computed in the next loop iteration
        cuda::memcpy_async(block, shared + shared_offset[copy_stage_idx], global_in + global_idx, sizeof(int) * block.size(), pipeline);
        // Collectively commit (advance) the pipeline's head stage
        pipeline.producer_commit();

        // Collectively wait for the operations commited to the
        // previous `compute` stage to complete:
        pipeline.consumer_wait();

        // Computation overlapped with the memcpy_async of the "copy" stage:
        compute(global_out + global_idx, shared + shared_offset[compute_stage_idx]);

        // Collectively release the stage resources
        pipeline.consumer_release();
    }

    // Compute the data fetch by the last iteration
    pipeline.consumer_wait();
    compute(global_out + block_batch(batch_sz-1), shared + shared_offset[(batch_sz - 1) % 2]);
    pipeline.consumer_release();
}


__global__ void dumb(int* buff) {
  printf("%d  %d  %d \n", blockIdx.x, blockDim.x, threadIdx.x);
}


int main() {
  cudaStream_t stream;
  cudaStreamCreate(&stream);

  int* global_in;
  int* global_out;
  cudaMalloc(&global_in, 8 * 4);
  cudaMalloc(&global_out, 8 * 4);

  const int num_blocks = 1;
  const int thread_per_block = 256;
  const int batch_sz = 1;
  const int size = num_blocks * thread_per_block * batch_sz;

  with_staging<<<num_blocks, thread_per_block, 1024, stream>>>(
    global_out, global_in, size, batch_sz);
  
  // dumb<<<1, 256, 1024, stream>>>(global_out);
  cudaStreamSynchronize(stream);
}