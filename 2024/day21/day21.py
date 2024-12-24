import re
import enum
from itertools import permutations
from functools import cache

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=21, block=True)

KEYS = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}


class DirectionPad(enum.Enum):
    UP = (0, 1)
    A = (0, 2)
    LEFT = (1, 0)
    DOWN = (1, 1)
    RIGHT = (1, 2)
    FORBIDDEN = (0, 0)


DIRECTION_MAP = {
    DirectionPad.LEFT: Direction.WEST,
    DirectionPad.UP: Direction.NORTH,
    DirectionPad.RIGHT: Direction.EAST,
    DirectionPad.DOWN: Direction.SOUTH,
}


KEY_MOVE_CACHE = {}
DIRECTION_MOVE_CACHE = {}


@cache
def valid_key(start, sequence):
    start = start.value
    for key in sequence:
        start = start + DIRECTION_MAP[key]
        if start == (0, 0):
            return False
    return True


@cache
def valid_letter(start, sequence):
    for key in sequence:
        start = start + DIRECTION_MAP[key]
        if start == (3, 0):
            return False
    return True


for a, b in permutations(KEYS.keys(), 2):
    d = []
    y, x = KEYS[a]
    ty, tx = KEYS[b]
    dy, dx = y - ty, x - tx
    y, x = ty, tx
    if dy > 0:
        d.extend([DirectionPad.UP] * abs(dy))
    if dx < 0:
        d.extend([DirectionPad.RIGHT] * abs(dx))
    if dy < 0:
        d.extend([DirectionPad.DOWN] * abs(dy))
    if dx > 0:
        d.extend([DirectionPad.LEFT] * abs(dx))

    KEY_MOVE_CACHE[a, b] = [
        (*sequence, DirectionPad.A)
        for sequence in set(permutations(d))
        if valid_letter(KEYS[a], sequence)
    ]
for a in KEYS.keys():
    KEY_MOVE_CACHE[a, a] = [(DirectionPad.A,)]


for a, b in permutations(DirectionPad, 2):
    d = []
    y, x = a.value
    ty, tx = b.value
    dy, dx = y - ty, x - tx
    y, x = ty, tx
    if dy > 0:
        d.extend([DirectionPad.UP] * abs(dy))
    if dx < 0:
        d.extend([DirectionPad.RIGHT] * abs(dx))
    if dy < 0:
        d.extend([DirectionPad.DOWN] * abs(dy))
    if dx > 0:
        d.extend([DirectionPad.LEFT] * abs(dx))

    DIRECTION_MOVE_CACHE[a, b] = [
        (*sequence, DirectionPad.A)
        for sequence in set(permutations(d))
        if valid_key(a, sequence)
    ]
for a in DirectionPad:
    DIRECTION_MOVE_CACHE[a, a] = [(DirectionPad.A,)]


@cache
def _shortest_length(code, layer):
    loc = DirectionPad.A
    length = 0
    for c in code:
        if layer == 0:
            length += len(DIRECTION_MOVE_CACHE[loc, c][0])
        else:
            length += min(
                _shortest_length(seq, layer - 1) for seq in DIRECTION_MOVE_CACHE[loc, c]
            )
        loc = c

    return length


def shortest_length(code, robots):
    loc = "A"
    length = 0
    for c in code:
        length += min(_shortest_length(seq, robots) for seq in KEY_MOVE_CACHE[loc, c])
        loc = c
    return length


def part_one(data):
    t = 0
    for code in data.splitlines():
        n = int(re.sub(r"[^0-9]", "", code))
        t += shortest_length(code, 1) * n
    return t


def part_two(data):
    t = 0
    for code in data.splitlines():
        n = int(re.sub(r"[^0-9]", "", code))
        t += shortest_length(code, 24) * n
    return t


print(part_one(data))
print(part_two(data))
