#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data


data = get_data(year=2022, day=4, block=True)
lines = data.splitlines()

t = 0

for line in lines:
    f, s = line.split(",")
    f_start, f_end = f.split("-")
    s_start, s_end = s.split("-")

    fs = set(range(int(f_start), int(f_end)+1))
    ss = set(range(int(s_start), int(s_end)+1))

    if fs.intersection(ss):
        t += 1

print(t)
