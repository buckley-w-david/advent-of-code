from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=17, block=True)


def count_combinations(target, containers):
    state = [0] * (target + 1)
    state[0] = 1
    for container in containers:
        for x in range(target, container - 1, -1):
            state[x] += state[x - container]
    return state[target]


def part_one(data):
    containers = tuple(sorted(int(line) for line in data.splitlines()))
    return count_combinations(150, containers)


def part_two(data):
    containers = tuple(sorted(int(line) for line in data.splitlines()))
    return count_combinations(150, containers)


print(part_one(data))
