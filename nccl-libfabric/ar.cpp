#include <iostream>
#include <cuda_runtime.h>
#include <mpi.h>
#include <nccl.h>


int getEnv(const char* key) {
  if (const char* env_p = std::getenv(key)) return atoi(env_p);
  return 0;
}


int main() {
  // MPI Init
  int provided;
  MPI_Init_thread(NULL, NULL, MPI_THREAD_MULTIPLE, &provided);

  // Get MPI size and rank
  int world_size, world_rank, local_size, local_rank;
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
  local_rank = getEnv("OMPI_COMM_WORLD_LOCAL_RANK");
  local_size = getEnv("OMPI_COMM_WORLD_LOCAL_SIZE");

  // Set cuda device
  cudaSetDevice(local_rank);

  // NCCL init
  ncclUniqueId nccl_id;
  ncclComm_t nccl_comm;
  if (world_rank == 0) {
    ncclGetUniqueId(&nccl_id);
  }
  MPI_Bcast((void*)&nccl_id, sizeof(nccl_id), MPI_BYTE, 0, MPI_COMM_WORLD);
  ncclCommInitRank(&nccl_comm, world_size, nccl_id, world_rank);

  // CUDA stream
  cudaStream_t cuda_stream;
  cudaStreamCreateWithFlags(&cuda_stream, cudaStreamNonBlocking);

  // AllReduce Parameters
  void *input, *output;
  size_t numel = 8;
  cudaMalloc(&input, numel*sizeof(float));
  cudaMalloc(&output, numel*sizeof(float));

  // AllReduce
  ncclAllReduce(input, output, numel, ncclFloat, ncclSum, nccl_comm, cuda_stream);
  cudaStreamSynchronize(cuda_stream);
  printf("[%d/%d] Done AR\n", world_rank, world_size);

  // finalize
  ncclCommDestroy(nccl_comm);
  MPI_Finalize();
}