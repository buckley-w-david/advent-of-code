from functools import cache

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=19, block=True)


@cache
def find_towels(options, target):
    for option in options:
        if option == target[: len(option)]:
            rest = target[len(option) :]
            if rest == "":
                return [option]
            elif m := find_towels(options, rest):
                return [option] + m
    return []


@cache
def count_arrangements(options, target):
    count = 0
    for option in options:
        if option == target[: len(option)]:
            rest = target[len(option) :]
            if rest == "":
                count += 1
            else:
                count += count_arrangements(options, rest)
    return count


def parse(data):
    ts, ds = data.split("\n\n")
    towels = tuple(ts.split(", "))
    designs = ds.splitlines()
    return towels, designs


def part_one(data):
    towels, designs = parse(data)

    return sum(1 for design in designs if find_towels(towels, design))


def part_two(data):
    towels, designs = parse(data)

    return sum(count_arrangements(towels, design) for design in designs)


print(part_one(data))
print(part_two(data))
