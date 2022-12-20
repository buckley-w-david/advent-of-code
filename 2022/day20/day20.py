#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

class Wrapper:
    def __init__(self, v):
        self.value = v

data = get_data(year=2022, day=20, block=True)
lines = data.splitlines()
key = 811589153
il = list(map(Wrapper, map(lambda n: n*key, map(int, lines))))
t = 0

size = len(il) - 1

result = il.copy()

for _ in range(10):
    for v in il:
        src = result.index(v)
        result.pop(src)
        dst = (src + v.value) % size
        result.insert(dst, v)

for i, v in enumerate(result):
    if v.value == 0:
        start = i
        break

a=(result[(start+1000) % len(result)])
b=(result[(start+2000) % len(result)])
c=(result[(start+3000) % len(result)])
print(a.value+b.value+c.value)
