from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=8, block=True)


def escape(s):
    ss = ""
    for c in s:
        if c == '"':
            ss += '\\"'
        elif c == "\\":
            ss += "\\\\"
        else:
            ss += c
    return '"' + ss + '"'


def part_one(data):
    length = 0

    for line in data.splitlines():
        length += len(line) - len(eval(line))

    return length


def part_two(data):
    length = 0

    for line in data.splitlines():
        length += len(escape(line)) - len(line)

    return length


print(part_one(data))
print(part_two(data))
