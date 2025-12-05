from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=2, block=True)


def part_one(data):
    total = 0
    for dims in map(ints, data.splitlines()):
        l, w, h = dims
        surface_area = 2 * l * w + 2 * w * h + 2 * h * l
        a, b = sorted(dims)[:2]
        total += surface_area + a * b
    return total


def part_two(data):
    total = 0
    for dims in map(ints, data.splitlines()):
        l, w, h = dims
        volume = l * w * h
        a, b = sorted(dims)[:2]
        total += volume + 2 * a + 2 * b
    return total


print(part_one(data))
print(part_two(data))
