import re

from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=1, block=True)

lookup = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

def to_i(s):
    if s.isdigit():
        return int(s)
    else:
        return lookup[s]

total = 0
for line in data.splitlines():
    digits = re.findall(fr"(?=(\d|{'|'.join(lookup.keys())}))", line)
    first, last = digits[0], digits[-1]
    total += 10*to_i(first) + to_i(last)

print(total)
