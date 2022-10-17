import os

files = os.listdir(os.getcwd())
for file in sorted(files):
    if file[-4:] == ".txt":
        with open(file, "r") as fh:
            lines = fh.readlines()
        
        time, cnt = 0, 0
        for l in lines:
            if l[-4:] == " ms\n":
                time += float(l.split()[-2])
                cnt += 1
        if cnt != 0:
            time /= cnt
            print(file, "%.0f ms" % (time))
