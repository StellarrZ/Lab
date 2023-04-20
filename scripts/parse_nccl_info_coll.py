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



def main():
    with open("/fsx/pzesheng/logs/nccl_info/sample_coll_z2.log", "r") as f:
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
            # for output buffer size
            if coll == "AllGather":
                size *= nranks
            info[coll][size].append(opCount)
    
    # ToDo: put in csv directly
    for coll, stripe in info.items():
        for size, nums in stripe.items():
            print("%14s, %12d, %d," % (coll, size, len(nums)), nums)



if __name__ == '__main__':
    main()