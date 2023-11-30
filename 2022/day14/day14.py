#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data


data = get_data(year=2022, day=14, block=True)
lines = data.splitlines()
isl = map(ints, lines)

occupied = set()

t = 0

try:
    from itertools import pairwise
except ImportError:
    from itertools import tee

    def pairwise(iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

for l in isl:
    points = chunk(l, 2)
    for (x1, y1), (x2, y2) in pairwise(points):
        if x1 != x2:
            occupied.update([(x, y1) for x in range(min(x1, x2), max(x1, x2)+1)])
        else:
            occupied.update([(x1, y) for y in range(min(y1, y2), max(y1, y2)+1)])

SAND = (500, 0)
max_y = max(occupied, key=lambda xy: xy[1])[1]
floor = max_y + 2

while True:
    sx, sy = (500, 0)
    dirty = True
    while dirty:
        dirty = False
        if (sx, sy+1) not in occupied and sy+1 != floor:
            sy += 1
            dirty = True
        elif (sx-1, sy+1) not in occupied and sy+1 != floor:
            sy += 1
            sx -= 1
            dirty = True
        elif (sx+1, sy+1) not in occupied and sy+1 != floor:
            sy += 1
            sx += 1
            dirty = True
    t += 1
    if (sx, sy) == SAND:
        break
    occupied.add((sx, sy))
print(t)
