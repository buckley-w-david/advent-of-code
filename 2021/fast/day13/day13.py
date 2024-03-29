#!/usr/bin/env python

from aocd import get_data, submit

import re

p = re.compile("fold along (x|y)=(\d+)")

data = get_data(year=2021, day=13, block=True)

dots, folds = data.split("\n\n")

dots = [tuple(map(int, i.split(","))) for i in dots.split("\n")]

folds2 = []
for fold in folds.split("\n"):
    m = p.match(fold)
    folds2.append((m.group(1), int(m.group(2))))

width = max(dots, key=lambda d: d[0])[0]+1
height = max(dots, key=lambda d: d[1])[1]+1

g = [[0 for _ in range(width)] for _ in range(height)]
for dot in dots:
    x, y = dot
    g[y][x] = 1

for fold in folds2:
    height = len(g)
    width = len(g[0])
    first = fold
    if first[0] == 'y':
        s = first[1]
        for y in range(s, height):
            for x in range(width):
                if g[y][x] == 1:
                    dy = y-s
                    g[s-dy][x] = 1
        g = [row for row in g[:s]] 
    else:
        s = first[1]
        for y in range(0, height):
            for x in range(s, width):
                if g[y][x] == 1:
                    dx = x-s
                    g[y][s-dx] = 1
        g = [[g[y][x] for x in range(s)] for y in range(height)]

for row in g:
    for col in row:
        print('#' if col else ' ', end='')
    print()
