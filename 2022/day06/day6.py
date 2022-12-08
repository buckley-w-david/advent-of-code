#!/usr/bin/env python

from aocd import get_data

data = get_data(year=2022, day=6, block=True)

for r in range(0, len(data)-14):
    packet = data[r:r+14]
    if len(set(packet)) == 14:
        print(r+14)
        break
