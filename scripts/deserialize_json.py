import os
import sys
import json


while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        continue
    monitor_data = json.loads(line)
    readable = json.dumps(monitor_data, indent=4)
    print(readable)
