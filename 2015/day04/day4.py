from aoc_utils import *
from aocd import get_data

from hashlib import md5

data = get_data(year=2015, day=4, block=True)


def part_one(data):
    i = 1
    while True:
        key = data + str(i)
        digest = md5(key.encode()).hexdigest()
        if digest[:5] == "00000":
            return i
        i += 1


def part_two(data):
    i = 1
    while True:
        key = data + str(i)
        digest = md5(key.encode()).hexdigest()
        if digest[:6] == "000000":
            return i
        i += 1


print(part_one(data))
print(part_two(data))
