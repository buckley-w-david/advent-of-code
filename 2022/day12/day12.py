#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

import string

data = get_data(year=2022, day=12, block=True)
lines = data.splitlines()

g = []

h = string.ascii_lowercase
start = None
end = None

for y in range(len(lines)):
    line = lines[y]
    l = []
    for x in range(len(line)):
        p = (y, x)
        item1 = line[x]
        if item1 == "S":
            start = p
            h1 = 0
        elif item1 == "E":
            end = p
            h1 = h.index("z")
        else:
            h1 = h.index(item1)
        l.append(h1)
    g.append(l)

grid = Grid(g)
g = Graph()
for p, h1 in grid.row_major_with_index():
    for q, h2 in grid.around_with_index(p, corners=False):
        if h2 - h1 <= 1:
            g.add_edge(p, q)

m = g.dijkstra(start).distance_to(end)
for p, h1 in grid.row_major_with_index():
    if h1 == 0:
        try:
            m = min(m, g.dijkstra(p).distance_to(end))
        except KeyError:
            pass
print(m)
