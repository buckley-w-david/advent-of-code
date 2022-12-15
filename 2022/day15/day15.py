#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data


data = get_data(year=2022, day=15, block=True)

lines = data.splitlines()
isl = map(ints, lines)

def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2-x1) + abs(y2-y1)

d = {}
for sx, sy, bx, by in isl:
    d[(sx, sy)] = (bx, by, dist((sx, sy), (bx, by)))

edge = 4000000

for (sx, sy), (_, _, r) in d.items():
    for t in range(r+1):
        for cx, cy in [( sx - r - 1 + t, sy - t ), ( sx - r - 1 + t, sy + t ), ( sx + r + 1 - t, sy - t ), ( sx + r + 1 - t, sy + t )]:
            if 0 <= cx <= edge and 0 <= cy <= edge:
                for sensor, (_, _, r) in d.items():
                    if dist((cx, cy), sensor) <= r:
                        break
                else:
                    print( cx * 4000000 + cy )
