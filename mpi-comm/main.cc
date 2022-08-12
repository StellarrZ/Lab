#include <iostream>
#include <vector>
#include <mpi.h>


int main() {
  int world_size, world_rank;
  MPI_Init(NULL, NULL);
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

  std::vector<int32_t> ranks;
  for (int32_t i = 0; i < world_size; i = i + 2) {
    ranks.push_back(i);
  }

  if ((world_rank % 2) == 0) {
    MPI_Group world_group, new_group;
    MPI_Comm_group(MPI_COMM_WORLD, &world_group);
    MPI_Group_incl(world_group, ranks.size(), ranks.data(), &new_group);

    MPI_Comm comm_all_ranks, comm_local_ranks;
    MPI_Comm_create_group(MPI_COMM_WORLD, new_group, 0, &comm_all_ranks);

    int color = 0;
    int key;
    MPI_Comm_rank(comm_all_ranks, &key);
    MPI_Comm_split(comm_all_ranks, color, key, &comm_local_ranks);

    std::cout << "  rank " << world_rank << "  key " << key << std::endl;

    int group_local_size, group_local_rank;
    MPI_Comm_size(comm_local_ranks, &group_local_size);
    MPI_Comm_rank(comm_local_ranks, &group_local_rank);

    std::cout << "  group_local_size " << group_local_size 
              << "  group_local_rank " << group_local_rank 
              << std::endl;
  }

  MPI_Finalize();

  return 0;
}