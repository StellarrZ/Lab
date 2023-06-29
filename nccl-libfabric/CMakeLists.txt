cmake_minimum_required(VERSION 2.8)
project(mpi_libfabric_intercept)

# set(NCCL_DIR /usr/local/cuda-11.8)
set(NCCL_DIR /fsx/users/sauron/local)

set(CUDA_USE_STATIC_CUDA_RUNTIME OFF)
find_package(CUDA REQUIRED)
# find_package(NCCL REQUIRED)
find_package(MPI REQUIRED)

include_directories(${CUDA_INCLUDE_DIRS})
# include_directories(${NCCL_INCLUDE_DIRS})
include_directories(${MPI_INCLUDE_PATH})

include_directories(${NCCL_DIR})

# add_executable(ar ar.cpp ${NCCL_DIR}/targets/x86_64-linux/include/nccl.h)
add_executable(ar ar.cpp ${NCCL_DIR}/include/nccl.h)
target_link_libraries(ar ${MPI_LIBRARIES} ${CUDA_LIBRARIES} ${NCCL_DIR}/lib/libnccl.so)


include_directories(/opt/amazon/efa/include)
add_library(mocker SHARED mocker.cpp)
target_link_libraries(mocker /opt/amazon/efa/lib64/libfabric.so)
