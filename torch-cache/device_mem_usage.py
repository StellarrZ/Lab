import os
import time
import subprocess
from signal import SIGTERM
import torch


def monitor_device_mem(interval=2):
    print("Querying nvidia-smi every %d seconds..." % interval)
    print("index, name, memory.total, memory.used")
    cmd = "nvidia-smi --query-gpu=index,name,memory.total,memory.used --format=csv -l %d | grep 0," % interval
    proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
    return os.getpgid(proc.pid)


def main():
    torch.cuda.set_device(0)
    tensor = torch.ones(10<<30, dtype=torch.int8, device="cuda", layout=torch.strided)
    print(" <<< Registered a 10GB tensor >>>")
    time.sleep(2)

    del tensor
    print(" <<< Destroyed the 10GB tensor >>>")
    time.sleep(6)

    tensor = torch.zeros(8<<30, dtype=torch.int8, device="cuda", layout=torch.strided)
    print(" <<< Registered a 8GB tensor >>>")
    time.sleep(6)

    del tensor
    tensor = torch.zeros(16<<30, dtype=torch.int8, device="cuda", layout=torch.strided)
    print(" <<< Destroyed the 8GB tensor and registered a 16GB tensor >>>")
    time.sleep(6)

    del tensor
    print(" <<< Destroyed the 16GB tensor >>>")
    time.sleep(6)

    tensor = torch.zeros(26<<30, dtype=torch.int8, device="cuda", layout=torch.strided)
    print(" <<< Registered a 26GB tensor >>>")
    time.sleep(6)

    del tensor
    print(" <<< Destroyed the 26GB tensor >>>")
    time.sleep(6)

    torch.cuda.empty_cache()
    print(" <<< Cleared PyTorch CUDA memory pool >>>")
    time.sleep(6)


if __name__ == "__main__":
    shell_pgid = monitor_device_mem()
    main()
    os.killpg(shell_pgid, SIGTERM)


# Sample output
'''
Querying nvidia-smi every 2 seconds...
index, name, memory.total, memory.used
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 5 MiB
 <<< Registered a 10GB tensor >>>
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 10801 MiB
 <<< Destroyed the 10GB tensor >>>
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 10801 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 10801 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 10801 MiB
 <<< Registered a 8GB tensor >>>
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 10801 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 10801 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 10801 MiB
 <<< Destroyed the 8GB tensor and registered a 16GB tensor >>>
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
 <<< Destroyed the 16GB tensor >>>
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
 <<< Registered a 26GB tensor >>>
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
 <<< Destroyed the 26GB tensor >>>
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 27185 MiB
 <<< Cleared PyTorch CUDA memory pool >>>
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 561 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 561 MiB
0, NVIDIA A100-SXM4-40GB, 40960 MiB, 561 MiB
'''
