from functools import reduce
from operator import mul, add
from collections import defaultdict

from aoc_utils.collections import transpose

with open("input.txt", "r") as f:
    data = f.read()


def parse_one(data):
    lines = data.splitlines()
    rows = [[int(n) for n in line.split()] for line in lines[:-1]]
    columns = transpose(rows)
    operators = [mul if c == "*" else add for c in lines[-1].split()]
    return columns, operators


def parse_two(data):
    lines = data.splitlines()
    cols = defaultdict(list)
    for line in lines[:-1]:
        for i in range(len(line)):
            cols[i].append(line[i])

    columns = []
    column = []
    for col in cols:
        num = "".join(cols[col]).strip()
        if num:
            column.append(int(num))
        else:
            columns.append(column)
            column = []
    columns.append(column)

    operators = iter([mul if c == "*" else add for c in lines[-1].split()])
    return columns, operators


def sum_equations(columns, operators):
    s = 0
    for op, column in zip(operators, columns):
        s += reduce(op, column)
    return s


def part_one(data):
    return sum_equations(*parse_one(data))


def part_two(data):
    return sum_equations(*parse_two(data))


print(part_one(data))
print(part_two(data))
