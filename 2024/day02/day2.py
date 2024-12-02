from aocd import get_data
from aoc_utils import *  # type: ignore

from itertools import pairwise

data = get_data(year=2024, day=2, block=True)


def safe(report):
    increasing = True
    decreasing = True
    rule = True
    for a, b in pairwise(report):
        increasing &= a > b
        decreasing &= a < b
        delta = abs(a - b)
        rule &= delta >= 1 and delta <= 3

    return (increasing or decreasing) and rule


def part_one(data):
    total = 0
    reports = [ints(l) for l in data.splitlines()]

    for report in reports:
        total += safe(report)

    return total


def part_two(data):
    total = 0
    reports = [ints(l) for l in data.splitlines()]

    for report in reports:
        if not safe(report):
            for i in range(len(report)):
                r = report[:i] + report[i + 1:]

                if safe(r):
                    total += 1
                    break
        else:
            total += 1

    return total


print(part_one(data))
print(part_two(data))
