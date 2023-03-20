#!/bin/bash

num_nodes=2

SMP_USER=pzesheng
CONTAINER_NAME="pt113-vit-base"
SM_OUTPUT_DATA_DIR="/tmp/random/"

export SMP_LOG_LEVEL="INFO"
export SM_HP_MP_PARAMETERS="{}"
TIME_STAMP=$( date +"%H%M%S_%Y-%m-%d" )
/fsx/pzesheng/scripts/my_smprun $SMP_USER -n $num_nodes -v --mpi-path /opt/amazon/openmpi/bin/mpirun \
        -d /fsx/pzesheng/Lab-Herring/torch-pgnccl -c $CONTAINER_NAME \
        -x SM_NUM_GPUS=8 -x SM_MODEL_DIR=$SM_OUTPUT_DATA_DIR -x SM_CHANNEL_TEST=$SM_CHANNEL_TEST -x SMP_MANUAL_INIT=1 \
        -x SM_CHANNEL_TRAIN=$SM_CHANNEL_TRAIN -x SM_OUTPUT_DATA_DIR=$SM_OUTPUT_DATA_DIR \
        -x SM_HP_MP_PARAMETERS=$SM_HP_MP_PARAMETERS \
        -x SMP_NCCL_THROTTLE_LIMIT=-1 \
        -x SMP_ENABLE_CROSS_NODE_D2D=0 -x SMP_D2D_GPU_BUFFER_SIZE_BYTES=1 \
        -x NCCL_ALGO=ring -x SMP_DISABLE_D2D=1 \
        -x HDF5_USE_FILE_LOCKING=FALSE \
        -x NCCL_DEBUG=WARN -x NCCL_PROTO=simple \
        -x MEM_EFFICIENT_LINEAR=1 -x PATH -x LD_LIBRARY_PATH \
        nsys profile -o /fsx/pzesheng/profile/${TIME_STAMP}-exp-%q{OMPI_COMM_WORLD_RANK}.qdrep --force-overwrite true \
        /opt/conda/bin/python /fsx/pzesheng/Lab-Herring/torch-pgnccl/exp.py

