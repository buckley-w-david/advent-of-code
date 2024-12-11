from collections import defaultdict
from math import log10

from aoc_utils import *  # type: ignore

data = "3935565 31753 437818 7697 5 38 0 123"


def count_rocks(rocks, iterations):
    # This implementation ignores the part of the problem that specifies that rocks maintain their ordering through iterations
    # This is fine because it doesn't actually have any effect on the data we're calculating (total number of rocks)
    for _ in range(iterations):
        nr = defaultdict(int)
        for rock, n in rocks.items():
            if rock == 0:
                nr[1] += rocks[rock]
            elif (ld := int(log10(rock)) + 1) % 2 == 0:
                half = 10 ** (ld // 2)
                right = rock % half
                left = rock // half
                nr[left] += n
                nr[right] += n
            else:
                nr[rock * 2024] += n
        rocks = nr

    return sum(rocks.values())


def part_one(data):
    rocks = {d: 1 for d in ints(data)}
    return count_rocks(rocks, 25)


def part_two(data):
    rocks = {d: 1 for d in ints(data)}
    return count_rocks(rocks, 75)


print(part_one(data))
print(part_two(data))
