from itertools import pairwise
import string

from aoc_utils import *
from aocd import get_data

CHARACTER_TO_INT = {}
INT_TO_CHARACTER = {}

for i, c in enumerate(string.ascii_lowercase):
    CHARACTER_TO_INT[c] = i
    INT_TO_CHARACTER[i] = c

data = get_data(year=2015, day=11, block=True)


def increment(password):
    idx = len(password) - 1
    while idx >= 0:
        password[idx] += 1
        if password[idx] == 26:
            password[idx] = 0
            idx -= 1
        else:
            break
    return password


def valid(password):
    if len(password) != 8:
        return False

    # We don't actually have to check this
    # because we never pass in a password with these characters
    # Doing it anyway for correctness
    for i in password:
        char = INT_TO_CHARACTER[i]
        if char == "i" or char == "o" or char == "l":
            return False

    straight = False
    for i in range(len(password) - 2):
        a, b, c = password[i: i + 3]
        straight |= b == a + 1 and c == b + 1

    if not straight:
        return False

    doubles = set()
    for a, b in pairwise(password):
        if a != b:
            continue

        doubles.add((a, b))

    return len(doubles) >= 2


def next_password(password):
    numeric = increment([CHARACTER_TO_INT[c] for c in password])

    while not valid(numeric):
        increment(numeric)

        # Shortcut super-increment if any digits are i, o, or l
        for idx, i in enumerate(numeric):
            char = INT_TO_CHARACTER[i]
            if char == "i" or char == "o" or char == "l":
                # We would normally have to worry about overflowing here
                # But none of the cases (i, o, or l) that trigger this would
                # overflow by adding 1
                numeric[idx] += 1
                for j in range(idx + 1, len(numeric)):
                    numeric[j] = 0

    return "".join(INT_TO_CHARACTER[i] for i in numeric)


def part_one(data):
    return next_password(data)


def part_two(data):
    return next_password(next_password(data))


print(part_one(data))
print(part_two(data))
