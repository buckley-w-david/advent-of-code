#!/usr/bin/env python

from aocd import get_data
from aoc_utils import Grid, Graph

data = get_data(year=2021, day=15, block=True)

rows = data.splitlines()
gg = [[int(c) for c in row] for row in rows]
lc = len(gg)
lr = len(gg[0])

grid = Grid([[0 for _ in range(lr*5)] for _ in range(lc*5)])
graph = Graph()

for yy in range(5):
    for xx in range(5):
        for y in range(lc):
            for x in range(lr):
                me = (y+yy*lc, x+xx*lr)
                cost = ((gg[y][x] - 1 + yy + xx) % 9) + 1

                for p, _ in grid.around_with_index(me, corners=False):
                    graph.add_edge(p, me, cost)

target = (grid.height-1, grid.width-1)
dij = graph.dijkstra((0, 0))
print(dij.distance_to(target))
