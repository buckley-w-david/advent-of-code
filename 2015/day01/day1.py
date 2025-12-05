from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=1, block=True)


def part_one(data):
    positon = 0
    for instruction in data:
        if instruction == "(":
            positon += 1
        elif instruction == ")":
            positon -= 1

    return positon


def part_two(data):
    positon = 0
    for i, instruction in enumerate(data):
        if instruction == "(":
            positon += 1
        elif instruction == ")":
            positon -= 1
        if positon < 0:
            return i + 1


print(part_one(data))
print(part_two(data))
