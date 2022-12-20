#!/usr/bin/env python

file = 'input.txt'
# file = 'example.txt'
with open(file, 'r') as f:
    raw_data = f.read()

key = 811589153
data = [key*int(s) for s in raw_data.splitlines()]
idx = list(range(len(data)))

def translate(data, idx):
    result = [0] * len(data)
    for i, j in enumerate(idx):
        result[j] = data[i]
    return result

for _ in range(10):
    for i in range(len(data)):
        src = idx[i]
        v = data[i]
        target = (src+v) % (len(data)-1)

        l = min(src, target)
        m = max(src, target)
        for j in range(len(idx)):
            if target > src:
                if l < idx[j] <= m:
                    idx[j] -= 1
            else:
                if l <= idx[j] < m:
                    idx[j] += 1
        idx[i] = target

result = translate(data, idx)
start = result.index(0)
print(sum(result[(start+v) % len(result)] for v in (1000, 2000, 3000)))
