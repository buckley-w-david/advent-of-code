#!/usr/bin/env python

from aocd import get_data
from aoc_utils import *

import math

data = get_data(year=2019, day=10)
lines = data.splitlines()
height = len(lines)
width = len(lines[0])

asteroids = { (y, x) for y, line in enumerate(lines) for x, c in enumerate(line) if c == '#' }

# As determined in pt 1
best = (14, 19)
y1, x1 = best
vectors = set()
for asteroid in asteroids - {best}:
    y2, x2 = asteroid
    dy, dx = abs(y2-y1), abs(x2-x1)
    gcd = math.gcd(dx, dy)

    dy //= gcd
    dx //= gcd
    if y2 < y1:
        dy *= -1
    if x2 < x1:
        dx *= -1
    vectors.add((dy, dx))

def zap_order(yx):
    oy, ox = yx

    # This effectivly rotates them like I want to to match atan2's behavious
    y, x = -ox, oy

    # this addition/modulus is to get (1,0) in the right place 
    return (math.atan2(y, x) + math.pi) % (2*math.pi)

vaporized_order = sorted(vectors, key=zap_order)

vaporized_asteroids = set()
order = []

zapped = True
while zapped:
    zapped = False
    for v in vaporized_order:
        dy, dx = v
        s = best
        while True:
            y, x = s
            x += dx
            y += dy
            s = (y, x)
            if s in asteroids and not s in vaporized_asteroids:
                zapped = True
                vaporized_asteroids.add(s)
                order.append(s)
                asteroids.remove(s)
                break
            if not (0 <= x < width and 0 <= y < height):
                break

y, x = order[199]
print(x*100 + y)
