import operator

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=7, block=True)


def operator_combinations(length, operators):
    if length == 1:
        for op in operators:
            yield [op]
    else:
        for combo in operator_combinations(length - 1, operators):
            for op in operators:
                yield [op] + combo


def calibration(equations, operators):
    s = 0
    for test, initial, *values in equations:
        posts = len(values)

        valid = False

        for combo in operator_combinations(posts, operators):
            value = initial

            for a, op in zip(values, combo):
                value = op(value, a)

            if value == test:
                valid = True
                break

        if valid:
            s += test

    return s


def part_one(data):
    equations = [ints(line) for line in data.splitlines()]

    return calibration(equations, [operator.add, operator.mul])


def concat(a, b):
    return int(str(a) + str(b))


def part_two(data):
    equations = [ints(line) for line in data.splitlines()]

    return calibration(equations, [operator.add, operator.mul, concat])


print(part_one(data))
print(part_two(data))
