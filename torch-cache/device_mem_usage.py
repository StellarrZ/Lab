import os
import time
import subprocess
from signal import SIGTERM
import torch


def monitor_device_mem(interval=2):
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
    print(" <<< Destroyed a 10GB tensor >>>")
    time.sleep(6)
    torch.cuda.empty_cache()
    print(" <<< Cleared PyTorch CUDA memory pool >>>")
    time.sleep(6)


if __name__ == "__main__":
    shell_pgid = monitor_device_mem()
    main()
    os.killpg(shell_pgid, SIGTERM)
