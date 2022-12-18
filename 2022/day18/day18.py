#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

from collections import deque

data = get_data(year=2022, day=18, block=True)
lines = data.splitlines()
isl = map(ints, lines)

occupied = set(map(tuple, isl))

def gx(p):
    return p[0]
def gy(p):
    return p[1]
def gz(p):
    return p[2]

min_x, max_x = min(occupied, key=gx)[0]-1, max(occupied, key=gx)[0]+1
min_y, max_y = min(occupied, key=gy)[1]-1, max(occupied, key=gy)[1]+1
min_z, max_z = min(occupied, key=gz)[2]-1, max(occupied, key=gz)[2]+1

start = (min_x, min_y, min_z)

queue = deque()
queue.appendleft(start)

history = set()
seen = 0
while queue:
    x, y, z = queue.pop()
    if x < min_x or x > max_x or y < min_y or y > max_y or z < min_z or z > max_z or (x, y, z) in history:
        continue
    history.add((x, y, z))

    for p in [(x+1, y, z),
            (x-1, y, z),
            (x, y+1, z),
            (x, y-1, z),
            (x, y, z+1),
            (x, y, z-1)]:
        if p in occupied:
            seen += 1
        else:
            queue.appendleft(p)
print(seen)
