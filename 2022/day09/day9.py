#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

data = get_data(year=2022, day=9, block=True)
lines = data.splitlines()

trail = [(0, 0)]*10

def tug(tail, head):
    ty, tx = tail
    hy, hx = head

    if abs(ty - hy) > 1:
        if hy > ty:
            ty += 1
        elif hy < ty:
            ty -= 1
        if hx > tx:
            tx += 1
        elif hx < tx:
            tx -= 1
    elif abs(tx - hx) > 1:
        if hy > ty:
            ty += 1
        elif hy < ty:
            ty -= 1
        if hx > tx:
            tx += 1
        elif hx < tx:
            tx -= 1
    return (ty, tx)

spaces = set([(0, 0)])
for line in lines:
    dir, amt = line.split()
    dy, dx = 0, 0
    if dir == "U":
        dy = -1
    elif dir == "D":
        dy = 1
    elif dir == "L":
        dx = -1
    elif dir == "R":
        dx = 1
    amt = int(amt)
    for _ in range(amt):
        y, x = trail[0]
        trail[0] = y+dy, x+dx
        for i in range(9):
            head, tail = trail[i], trail[i+1]
            trail[i+1] = tug(tail, head)
        spaces.add(trail[-1])
print(len(spaces))
