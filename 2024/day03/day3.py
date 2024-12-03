import re

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=3, block=True)


def part_one(data):
    instructions = re.findall(r"mul\((\d+),(\d+)\)", data)
    total = 0

    for a, b in instructions:
        total += int(a) * int(b)

    return total


def part_two(data):
    instructions = re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", data)
    enable = True
    total = 0

    for instruction in instructions:
        if instruction == "do()":
            enable = True
        elif instruction == "don't()":
            enable = False
        elif enable:
            a, b = ints(instruction)
            total += a * b

    return total


print(part_one(data))
print(part_two(data))
