import torch
from torch.utils import benchmark


def main():
    dtype = torch.float16
    n = 16 << 10
    a = torch.randn(n, n).type(dtype).cuda()
    b = torch.randn(n, n).type(dtype).cuda()

    t = benchmark.Timer(stmt='a @ b', globals={'a': a, 'b': b})

    x = t.timeit(50)
    print(2 * n ** 3 / x.median / 1e12)


if __name__ == "__main__":
    main()

    # A100 40GB: ~267
