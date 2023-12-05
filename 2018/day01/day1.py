from itertools import cycle
from aoc_utils import *
from aocd import get_data

data = get_data(year=2018, day=1, block=True)

def part_one(data):
    return sum(ints(data))

def part_two(data):
    s = 0
    history = {0}
    for n in cycle(ints(data)):
        s += n
        if s in history:
            return s
        history.add(s)

print(part_one(data))
print(part_two(data))
