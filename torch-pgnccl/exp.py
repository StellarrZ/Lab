import os
import time
import numpy as np
import torch
import torch.distributed as dist
from torch.distributed import ReduceOp
# import smdistributed.dataparallel.torch.torch_smddp


dist.init_process_group(backend="nccl")


local_rank = int(os.getenv("OMPI_COMM_WORLD_LOCAL_RANK"))
world_rank = int(os.getenv("OMPI_COMM_WORLD_RANK"))
world_size = int(os.getenv("OMPI_COMM_WORLD_SIZE"))

device = torch.device("cuda")
torch.cuda.set_device(local_rank)
stream_1 = torch.cuda.Stream(local_rank)
stream_2 = torch.cuda.Stream(local_rank)
# torch.cuda.set_stream(stream_1)

# ar_tensor = torch.ones(1, 1, device=device) * world_rank
ag_tensor = torch.ones(1, 1, device=device) * world_rank
# ag_result = [torch.zeros(1, 1, device=device) for _ in range(world_size)]
ag_result = torch.zeros(1, world_size, device=device)

for i in range(10):
    torch.cuda.set_stream(stream_1)
    ar_tensor = torch.ones(1, 1, device=device) * world_rank
    ar = dist.all_reduce(ar_tensor, async_op=True)
    torch.cuda.set_stream(stream_2)
    # ag = dist.all_gather(ag_result, ag_tensor, async_op=True)
    ag = dist.all_gather_into_tensor(ag_result, ag_tensor, async_op=True)
    ar.wait()
    ag.wait()


# dist.barrier()
# time.sleep(2)
print(ar_tensor)
print(ag_result)
