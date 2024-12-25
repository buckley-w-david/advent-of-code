from itertools import product

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=25, block=True)


def part_one(data):
    schematics = data.split("\n\n")
    keys = []
    locks = []
    for schematic in schematics:
        heights = [-1] * 5
        for line in schematic.splitlines():
            for i, c in enumerate(line):
                heights[i] += c == "#"

        if schematic[:5] == "#####":
            locks.append(tuple(heights))
        else:
            keys.append(tuple(heights))

    t = 0
    for key, lock in product(keys, locks):
        for kh, hl in zip(key, lock):
            if kh + hl > 5:
                break
        else:
            t += 1
    return t


print(part_one(data))
