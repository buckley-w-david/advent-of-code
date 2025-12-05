from collections import Counter
from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=3, block=True)


def part_one(data):
    x, y = 0, 0
    counts = Counter()
    counts[(0, 0)] = 1
    for d in data:
        match d:
            case ">":
                x += 1
            case "<":
                x -= 1
            case "^":
                y += 1
            case "v":
                y -= 1
        counts[(x, y)] += 1

    return len(counts)


def part_two(data):
    pos = [[0, 0], [0, 0]]
    counts = Counter()
    counts[(0, 0)] = 2
    for i, d in enumerate(data):
        idx = i % 2 == 0
        santa = pos[idx]
        match d:
            case ">":
                santa[0] += 1
            case "<":
                santa[0] -= 1
            case "^":
                santa[1] += 1
            case "v":
                santa[1] -= 1

        counts[(santa[0], santa[1])] += 1

    return len(counts)


print(part_one(data))
print(part_two(data))
