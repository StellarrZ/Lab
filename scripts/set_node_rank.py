import os

with os.popen("hostname") as f:
    hostname = f.readline()
    nid = int(hostname.strip().split("-")[-1])

with os.popen("cat ~/smddpjobs/allotment/pzesheng") as f:
    s = f.readline()
    s = s.strip().rstrip("]")
    l = s[s.find("[") + 1:].split(",")

cnt, node = 0, None
for s in l:
    pair = s.split("-")
    if len(pair) == 2:
        for i in range(int(pair[0]), int(pair[1]) + 1):
            if i == nid:
                node = cnt
            cnt += 1
    elif len(pair) == 1:
        if int(pair[0]) == nid:
            node = cnt
        cnt +=1
    else:
        exit(1)

with open("/tmp/node_rank.txt", "w") as f:
    f.write("%d" % node)
