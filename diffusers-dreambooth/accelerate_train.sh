#!/bin/bash

python3 /fsx/pzesheng/Lab-Herring/scripts/dist_accelerate_config.py \
    --base_config /fsx/pzesheng/diffusers/examples/dreambooth/accelerate_config.yaml \
    --hostfile /fsx/pzesheng/hostfile \
    --local_config /tmp/default_config_$SLURM_NODEID.yaml

cat /tmp/default_config_$SLURM_NODEID.yaml
echo


export MODEL_NAME="CompVis/stable-diffusion-v1-4"
export INSTANCE_DIR=/fsx/pzesheng/samples/
export OUTPUT_DIR=/fsx/pzesheng/ck/

# export ACCELERATE_USE_SAGEMAKER="true"
# export ACCELERATE_SAGEMAKER_DISTRIBUTED_TYPE="DATA_PARALLEL"

accelerate launch \
    --config_file /tmp/default_config_$SLURM_NODEID.yaml \
    --debug \
/fsx/pzesheng/diffusers/examples/dreambooth/train_dreambooth.py \
    --pretrained_model_name_or_path=$MODEL_NAME  \
    --instance_data_dir=$INSTANCE_DIR \
    --output_dir=$OUTPUT_DIR \
    --instance_prompt='a,photo,of,sks,dog' \
    --resolution=512 \
    --train_batch_size=1 \
    --gradient_accumulation_steps=1 \
    --learning_rate=5e-6 \
    --lr_scheduler="constant" \
    --lr_warmup_steps=0 \
    --max_train_steps=400
