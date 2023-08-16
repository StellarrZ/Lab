#!/bin/bash

cd /home/ubuntu/pzesheng/EFAHealthCheckerInit
mkdir -p build && cd build
rm -r *
cmake ../ -DENABLE_CUDA=OFF -DBUILD_TEST=ON
make -j $( nproc )

pip3 install --user -r ./test/requirements.txt
