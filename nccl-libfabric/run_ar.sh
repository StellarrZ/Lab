#!/bin/bash

# export NCCL_DEBUG=INFO
# export NCCL_DEBUG=WARN
export NCCL_DEBUG=TRACE
export NCCL_DEBUG_SUBSYS=COLL
export FI_PROVIDER=efa
export FI_EFA_FORK_SAFE=1
export FI_EFA_USE_DEVICE_RDMA=1
export LD_PRELOAD=/fsx/users/sauron/Lab-Herring/nccl-libfabric/build/libmocker.so

/fsx/users/sauron/Lab-Herring/nccl-libfabric/build/ar