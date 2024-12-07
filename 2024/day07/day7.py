from math import log10
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
                if value > test:
                    break

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
    return a * (10 ** (int(log10(b)) + 1)) + b


def part_two(data):
    equations = [ints(line) for line in data.splitlines()]

    return calibration(equations, [operator.add, operator.mul, concat])


# Alternate implementations that are much faster
# I believe this is due to not having to do all the list construction and concatenation
# that ends up happening in operator_combinations


def valid(test, values, operators):
    def _valid(current, values):
        if len(values) == 0:
            return current == test

        for op in operators:
            if _valid(op(current, values[0]), values[1:]):
                return True

        return False

    return _valid(0, values)


def part_one_alt(data):
    equations = [ints(line) for line in data.splitlines()]

    v = 0
    for test, *values in equations:
        if valid(test, values, [operator.add, operator.mul]):
            v += test

    return v


def part_two_alt(data):
    equations = [ints(line) for line in data.splitlines()]

    v = 0
    for test, *values in equations:
        if valid(test, values, [operator.add, operator.mul, concat]):
            v += test

    return v


print(part_one_alt(data))
print(part_two_alt(data))
