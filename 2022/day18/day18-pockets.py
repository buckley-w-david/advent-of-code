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

directions = [
    ( 1,  0,  0),
    (-1,  0,  0),
    ( 0,  1,  0),
    ( 0, -1,  0),
    ( 0,  0,  1),
    ( 0,  0, -1),
]
min_x, max_x = min(occupied, key=gx)[0], max(occupied, key=gx)[0]
min_y, max_y = min(occupied, key=gy)[1], max(occupied, key=gy)[1]
min_z, max_z = min(occupied, key=gz)[2], max(occupied, key=gz)[2]

def oob(p):
    x, y, z = p
    return x < min_x or x > max_x or y < min_y or y > max_y or z < min_z or z > max_z

def adj(p):
    x, y, z = p
    for (dx, dy, dz) in directions:
        yield (x+dx, y+dy, z+dz)

air_pocket = set()
outside_air = set()

for cx in range(min_x, max_x+1):
    for cy in range(min_y, max_y+1):
        for cz in range(min_z, max_z+1):
            candidate = (cx, cy, cz)
            if candidate in occupied or candidate in air_pocket or candidate in outside_air:
                continue
            history = set([candidate])
            queue = deque([candidate])
            while queue:
                p = queue.pop()
                if oob(p):
                    outside_air.update(history)
                    break

                for pp in adj(p):
                    if pp not in occupied and pp not in history:
                        history.add(pp)
                        queue.appendleft(pp)
            else:
                air_pocket.update(history)

exposed_area = 6 * len(lines)
for p in occupied:
    for pp in adj(p):
        if pp in occupied or pp in air_pocket:
            exposed_area -= 1

print(exposed_area)
