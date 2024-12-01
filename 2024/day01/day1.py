from collections import Counter

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=1, block=True)


def part_one(data):
    aa, bb = [], []
    for line in data.splitlines():
        a, b = ints(line)
        aa.append(a)
        bb.append(b)

    aa, bb = sorted(aa), sorted(bb)

    distance = 0
    for a, b in zip(aa, bb):
        distance += abs(a - b)

    return distance


def part_two(data):
    aa, bb = [], []
    for line in data.splitlines():
        a, b = ints(line)
        aa.append(a)
        bb.append(b)

    cb = Counter(bb)

    score = 0
    for a in aa:
        score += a * cb[a]

    return score


print(part_one(data))
print(part_two(data))
