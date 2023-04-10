allot = "compute-st-worker-[2-17,32,69-75]"

s = allot.strip().rstrip("]")
l = s.split("[")

prefix = l[0]
l = l[1].split(",")
for s in l:
    pair = s.split("-")
    if len(pair) == 1:
        print(prefix + pair[0])
    elif len(pair) == 2:
        for i in range(int(pair[0]), int(pair[1]) + 1):
            print(prefix + str(i))

