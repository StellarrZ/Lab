import os
import deepspeed
import torch
import transformers
from transformers import (
    AutoModelForCausalLM,
    GPT2Config,
    GPT2LMHeadModel,
)


# def get_param_groups_by_weight_decay(module):
#     """Get param groups."""
#     weight_decay_params = {"params": []}
#     no_weight_decay_params = {"params": [], "weight_decay": 0.0}
#     param_ids = set()
#     for module_ in module.modules():
#         for n, p in list(module_._parameters.items()):
#             if p is not None and n != "bias" and id(p) not in param_ids:
#                 weight_decay_params["params"].append(p)
#                 param_ids.add(id(p))
#         for n, p in list(module_._parameters.items()):
#             if p is not None and n == "bias" and id(p) not in param_ids:
#                 no_weight_decay_params["params"].append(p)
#                 param_ids.add(id(p))
#     return weight_decay_params, no_weight_decay_params


deepspeed.init_distributed(dist_backend="nccl")

model_config = GPT2Config(
    vocab_size=50257,
    n_positions=4096,
    n_embd=6144,
    n_layer=32,
    n_head=48,
    n_inner=None,
    activation_function="gelu_new",
    layer_norm_epsilon=1e-05,
    summary_type="cls_index",
    summary_use_proj=True,
    summary_activation=None,
    summary_proj_to_labels=True,
    gradient_checkpointing=True,
    use_cache=False,
    bos_token_id=50256,
    eos_token_id=50256,
    return_dict=True,
)

with deepspeed.zero.Init(dtype=torch.bfloat16):
    model = AutoModelForCausalLM.from_config(model_config)

# param_groups = get_param_groups_by_weight_decay(model)
# optimizer = torch.optim.AdamW(param_groups)
optimizer = None

model, optimizer, _, _ = deepspeed.initialize(
    model=model,
    optimizer=optimizer,
    model_parameters=model.parameters(),
    config="/fsx/pzesheng/ds_config.json",
)

print("DONE INIT")
