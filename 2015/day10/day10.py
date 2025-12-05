import string

from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=10, block=True)


def speak_and_say(n):
    cur = n[0]
    out = []
    chunk = []
    for c in n:
        if c == cur:
            chunk.append(c)
        else:
            out.append(str(len(chunk)))
            out.append(chunk[0])
            chunk = [c]
            cur = c

    out.append(str(len(chunk)))
    out.append(chunk[0])

    return "".join(out)


def part_one(data):
    number = data

    for _ in range(40):
        number = speak_and_say(number)

    return len(number)


def part_two(data):
    number = data

    for _ in range(50):
        number = speak_and_say(number)

    return len(number)


print(part_one(data))
print(part_two(data))
