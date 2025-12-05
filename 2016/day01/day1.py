import re

from aoc_utils import *
from aocd import get_data

data = get_data(year=2016, day=1, block=True)


def part_one(data):
    pos = (0, 0)
    d = Direction.NORTH
    for m in re.findall(r"L\d+|R\d+", data):
        if m[0] == "R":
            d = d.rotate(cardinal=True)
        else:
            d = d.rotate(handedness=-1, cardinal=True)
        for _ in range(int(m[1:])):
            pos = pos + d
    return sum(map(abs, pos))


def part_two(data):
    pos = (0, 0)
    d = Direction.NORTH
    seen = set()
    for m in re.findall(r"L\d+|R\d+", data):
        if m[0] == "R":
            d = d.rotate(cardinal=True)
        else:
            d = d.rotate(handedness=-1, cardinal=True)
        for _ in range(int(m[1:])):
            pos = pos + d

            if pos in seen:
                return sum(map(abs, pos))
            seen.add(pos)


print(part_one(data))
print(part_two(data))
