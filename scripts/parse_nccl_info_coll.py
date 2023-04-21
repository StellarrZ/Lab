import os
from collections import defaultdict



class DefaultDictList(defaultdict):
    def __init__(self):
        super().__init__(list)


def sizeof_nccl_datatype(datatype):
    enum = int(datatype)
    if enum in (0, 1):
        return 1
    elif enum in (6, 9):
        return 2
    elif enum in (2, 3, 7):
        return 4
    elif enum in (4, 5, 8):
        return 8
    else:
        return -1


def size_bytes_to_str(size):
    i = 0
    units = ("  B", " KB", " MB", " GB")
    quo, rem = size, 0
    while not rem:
        size_str = str(quo) + units[i]
        i += 1
        quo, rem = divmod(quo, 1024)
    return size_str


# in-place modify
def ignore_init(info):
    bcastNumMax = "-1"
    for nums in info["Broadcast"].values():
        bcastNumMax = max([bcastNumMax] + nums, key=(lambda x: int(x, 16)))
    info.pop("Broadcast")

    watershed = int(bcastNumMax, 16)
    for coll, stripe in info.items():
        # ToDo: differentiate opCount by comm/stream address
        if coll != "AllGather":
            continue
        for size, nums in stripe.items():
            # searchable here
            while nums and int(nums[0], 16) <= watershed:
                nums.pop(0)
            if not nums:
                stripe.pop(size)
        if not coll:
            info.pop(coll)



def log2csv(fname):
    with open(os.path.join(path, fname + ".log"), "r") as f:
    # with open("/fsx/pzesheng/logs/nccl_info/sample_coll.log", "r") as f:
        lines = f.readlines()

    info = defaultdict(DefaultDictList)
    sign = " NCCL INFO "
    for l in lines:
        if sign in l:
            raw = l[l.find(sign) + len(sign):].strip().split()
            coll = raw[0].rstrip(":")
            
            i = 1
            while i < len(raw):
                if raw[i] == "opCount":
                    opCount = raw[i + 1]
                # elif raw[i] == "sendbuff":
                #     pass
                # elif raw[i] == "recvbuff":
                #     pass
                elif raw[i] == "count":
                    count = int(raw[i + 1])
                elif raw[i] == "datatype":
                    datatype = int(raw[i + 1])
                # elif raw[i] == "op":
                #     pass
                # elif raw[i] == "root":
                #     pass
                elif "nranks" in raw[i]:
                    nranks = int(raw[i].lstrip("[nranks=").rstrip("]"))
                # elif raw[i] == "stream":
                #     pass
                i += 2
            
            size = count * sizeof_nccl_datatype(datatype)
            # for global buffer size
            # i.e., AG output, RS input
            if coll in ("AllGather", "ReduceScatter"):
                size *= nranks
            info[coll][size].append(opCount)
    
    # remove init colls
    ignore_init(info)
    
    with open(os.path.join(path, fname + ".csv"), "w") as f:
        for coll, stripe in info.items():
            for size, nums in stripe.items():
                # csv format:
                # collName, globalBufferSize, count, [opCount, ...]
                size_str = size_bytes_to_str(size)
                print("%14s, %12s, %6d" % (coll, size_str, len(nums)), *nums, sep=", ", file=f)
                # print("%14s, %12d, %6d" % (coll, size, len(nums)), *nums, sep=", ", file=f)


if __name__ == '__main__':
    # path = "/fsx/pzesheng/logs/nccl_info/size_passes/15b_z3"
    # path = "/fsx/pzesheng/logs/nccl_info/size_passes/30b_z3"
    # path = "/fsx/pzesheng/logs/nccl_info/size_passes/65b_z3"
    path = "/fsx/pzesheng/logs/nccl_info/size_passes/95b_z3"
    for fname in os.listdir(path):
        if fname[-4:] == ".log":
            log2csv(fname[:-4])
