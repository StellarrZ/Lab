import os
import time
import numpy as np
import torch
import torch.distributed as dist
from torch.distributed import ReduceOp
import argparse



def partition(fn):
    res = fn()
    torch.cuda.Event(enable_timing=False).record()
    torch.cuda.synchronize()
    return res


# @partition
def func(stream_1=torch.cuda.default_stream(),
         stream_2=torch.cuda.default_stream(), pg_ar=None, pg_ag=None, n=5):
    for i in range(n):
        torch.cuda.set_stream(stream_1)
        ar_tensor = torch.ones(1, 1, device=device) * world_rank
        ar = dist.all_reduce(ar_tensor, op=ReduceOp.SUM, async_op=True, group=pg_ar)
        torch.cuda.set_stream(stream_2)
        ag = dist.all_gather_into_tensor(ag_output, ag_input, async_op=True, group=pg_ag)
        ar.wait()
        ag.wait()
    return ar_tensor, ag_output


def main():
    stream_default = torch.cuda.default_stream(local_rank)
    stream_1, stream_2 = torch.cuda.Stream(local_rank), torch.cuda.Stream(local_rank)

    pg_default = None
    pg_a, pg_b = dist.new_group(), dist.new_group()
    # Trigger PG lazy initializaion here to make profile more meaningful
    dist.barrier(group=pg_default)
    dist.barrier(group=pg_a)
    dist.barrier(group=pg_b)

    if args.experiment == 0:
        func(stream_1=stream_default, stream_2=stream_default, pg_ar=pg_default, pg_ag=pg_default)
        func(stream_1=stream_default, stream_2=stream_default, pg_ar=pg_a, pg_ag=pg_a)
        func(stream_1=stream_1, stream_2=stream_1, pg_ar=pg_a, pg_ag=pg_a)
    elif args.experiment == 1:
        func(stream_1=stream_1, stream_2=stream_2, pg_ar=pg_a, pg_ag=pg_a)
    elif args.experiment == 2:
        func(stream_1=stream_default, stream_2=stream_default, pg_ar=pg_default, pg_ag=pg_b)
        func(stream_1=stream_default, stream_2=stream_default, pg_ar=pg_a, pg_ag=pg_default)
        func(stream_1=stream_default, stream_2=stream_default, pg_ar=pg_a, pg_ag=pg_b)
        func(stream_1=stream_1, stream_2=stream_1, pg_ar=pg_a, pg_ag=pg_b)
    elif args.experiment == 3:
        func(stream_1=stream_1, stream_2=stream_2, pg_ar=pg_a, pg_ag=pg_b)
    else:
        pass



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--master-addr", default="10.10.16.77", type=str)
    parser.add_argument("--master-port", default="12345", type=str)
    parser.add_argument("--experiment", default=3, type=int)
    args, _ = parser.parse_known_args()

    local_rank = int(os.getenv("OMPI_COMM_WORLD_LOCAL_RANK"))
    world_rank = int(os.getenv("OMPI_COMM_WORLD_RANK"))
    world_size = int(os.getenv("OMPI_COMM_WORLD_SIZE"))

    os.environ["RANK"] = str(world_rank)
    os.environ["WORLD_SIZE"] = str(world_size)
    os.environ["MASTER_ADDR"] = args.master_addr
    os.environ["MASTER_PORT"] = args.master_port

    dist.init_process_group(backend="nccl")
    device = torch.device("cuda")
    torch.cuda.set_device(local_rank)

    ag_input = torch.ones(1, 1, device=device) * world_rank
    ag_output = torch.zeros(1, world_size, device=device)
    main()
