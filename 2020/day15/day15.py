#!/usr/bin/env python

from collections import defaultdict
from aocd import get_data, submit

data = get_data(year=2020, day=15, block=True)
# data = "0,3,6"
starting_numbers = [int(n) for n in data.split(",")]
history = defaultdict(int)
for i, n in enumerate(starting_numbers[:-1]):
    history[n] = i+1

last = -1
current = starting_numbers[-1]
for turn in range(len(starting_numbers), 30000001):
    last = current
    if current not in history:
        history[current] = turn
        current = 0
    else:
        tc = turn-history[current]
        history[current] = turn
        current = tc
print(last)
