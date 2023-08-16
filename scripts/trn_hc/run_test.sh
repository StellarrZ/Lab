#!/bin/bash

# echo "SLURM_NNODES  $SLURM_NNODES"
# echo "SLURM_NODEID  $SLURM_NODEID"

cd /home/ubuntu/pzesheng/EFAHealthCheckerInit/build
pytest ./test/test_driver.py --multi_node --projection host --server_addr 26.0.161.106 --size $SLURM_NNODES --rank $SLURM_NODEID
