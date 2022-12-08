#!/usr/bin/env python

from aocd import get_data, submit

print("\033[2J\033[H") # ]]

data = get_data(year=2020, day=17, block=True)
#data = """
#.#.
#..#
####
#""".strip()
print(data)
active = set()

def around(p):
    w, x, y, z = p
    for ww in range(-1, 2):
        for xx in range(-1, 2):
            for yy in range(-1, 2):
                for zz in range(-1, 2):
                    yield (w+ww, x+xx, y+yy, z+zz)

for y, row in enumerate(data.splitlines()):
    for x, col in enumerate(row):
        if col == '#':
            active.add((0, x, y, 0))

from more_itertools import flatten
for _ in range(6):
    next_gen = set()
    points_of_interest = flatten(map(around, active))
    for p in points_of_interest:
        p_active = p in active
        c = len(active.intersection(around(p))) - int(p_active)
        if c == 3 or (p_active and c == 2):
            next_gen.add(p)
    active = next_gen

print(len(active))
