#include<cstdio>
#include<mpi.h>


int main() {
    int size, rank = -1;
    MPI_Init(NULL, NULL);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    printf("SIZE %d  RANK %d\n", size, rank);

    MPI_Finalize();
    return 0;
}