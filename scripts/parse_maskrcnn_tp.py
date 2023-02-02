import os
import re
import sys


pattern = re.compile("throughput: (.*?) FPS")
summ, cnt = 0, 0
with open(sys.argv[1], 'r') as f:
    for line in f.readlines():
        res = pattern.search(line)
        if res:
          cnt += 1
          summ += float(res.groups()[0])

out = summ / cnt if cnt else pattern.pattern + "\nAbove Pattern Not Found"
print(out)
