import os
import torch
import torch.distributed as dist
from torch.distributed import ReduceOp
# import smdistributed.dataparallel.torch.torch_smddp


def run_all_reduce(async_op=False):
    tensor = torch.tensor([local_rank] * world_size).cuda()
    print(tensor)
    handle = dist.all_reduce(tensor, op=ReduceOp.SUM, async_op=async_op)
    if handle:
        handle.wait()
    print(tensor)
    

def run_barrier(device_ids=None, async_op=False):
    handle = dist.barrier(device_ids=device_ids, async_op=False)
    if handle:
        handle.wait()
    print("Done barrier")


local_rank = int(os.getenv("OMPI_COMM_WORLD_LOCAL_RANK"))
local_size = int(os.getenv("OMPI_COMM_WORLD_LOCAL_SIZE"))
world_rank = int(os.getenv("OMPI_COMM_WORLD_RANK"))
world_size = int(os.getenv("OMPI_COMM_WORLD_SIZE"))
torch.cuda.set_device(local_rank)
device = torch.device("cuda", local_rank)
dist.init_process_group(backend="nccl")
# dist.init_process_group(backend="smddp")


run_all_reduce(async_op=True)    
run_barrier(async_op=True)
run_barrier(device_ids=[local_rank], async_op=True)
run_barrier(device_ids=[x for x in range(local_size) if x % 2 == local_rank % 2], async_op=True)
run_barrier(device_ids=[(local_rank + 1) % local_size], async_op=True)
