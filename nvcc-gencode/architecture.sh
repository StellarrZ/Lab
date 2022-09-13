#!/bin/bash

SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TOOL_DIR=${SRC_DIR}/nv_architecture.cu
NVCC_DIR="$( which nvcc )"
EXEC_DIR=${SRC_DIR}/nv_architecture_temp

${NVCC_DIR} ${TOOL_DIR} -o ${EXEC_DIR}
${EXEC_DIR}
rm ${EXEC_DIR}