#!/usr/bin/env python

from aocd import get_data, submit
from aoc_utils import Grid, Direction
import itertools

data = get_data(year=2020, day=11, block=True)
# data = """
# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL
# """.strip()

decode = {
    ".": 0,
    "L": 1,
    "#": 2,
}

grid = Grid([[decode[s] for s in row] for row in data.split("\n")])
from pprint import pprint


old_changes = []
changes = []
first = True
# Sometimes I really with I had do-while loops
while changes or first:
    changes = []
    first = False
    for (yx, position) in grid.row_major_with_index():
        seen = []
        for dir in Direction:
            try:
                f = next(itertools.dropwhile(lambda p: p == 0, grid.ray_from(yx, dir)))
                seen.append(f)
            except StopIteration:
                pass
        occupied = [s for s in seen if s == 2]

        if position == 1:
            if not occupied:
                changes.append((yx, 2))
        elif position == 2:
            if len(occupied) >= 5:
                changes.append((yx, 1))

    for (yx, n) in changes:
        grid[yx] = n

print(len([i for i in grid if i == 2]))
