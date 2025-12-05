from aoc_utils import *
from aocd import get_data

data = get_data(year=2016, day=2, block=True)

DM = {
    "U": Direction.NORTH,
    "D": Direction.SOUTH,
    "R": Direction.EAST,
    "L": Direction.WEST,
}

NUMPAD = Grid([["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]])

DIAMOND_NUMPAD = Grid(
    [
        [None, None, "1", None, None],
        [None, "2", "3", "4", None],
        ["5", "6", "7", "8", "9"],
        [None, "A", "B", "C", None],
        [None, None, "D", None, None],
    ]
)


def decode(data, start, numpad):
    pos = start
    code = []
    for line in data.splitlines():
        for c in line:
            if numpad.get(p := pos + DM[c]):
                pos = p
        code.append(numpad[pos])
    return "".join(code)


def part_one(data):
    return decode(data, (1, 1), NUMPAD)


def part_two(data):
    return decode(data, (2, 0), DIAMOND_NUMPAD)


print(part_one(data))
print(part_two(data))
