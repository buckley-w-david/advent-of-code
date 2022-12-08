#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

data = get_data(year=2022, day=3, block=True)
lines = data.splitlines()

t = 0

for a, b, c in chunk(lines, 3):
    sa, sb, sc = set(a), set(b), set(c)

    common = sa.intersection(sb).intersection(sc).pop()
    if common.islower():
        prior = ord(common) - ord('a') + 1
    else:
        prior = ord(common) - ord('A') + 27
    t += prior

print(t)
