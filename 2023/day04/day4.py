from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=4, block=True)
lines = data.splitlines()

def winning_matches(line: str) -> int:
    win, have = line.split("|")
    return len(set(ints(win)[1:]) & set(ints(have)))

def part_one(data):
    s = 0
    for line in data.splitlines():
        matches = winning_matches(line)
        if matches > 0:
            s += 2**(matches-1)
    return s

def part_two(data):
    lines = data.splitlines()
    counts = [0]*len(lines)
    for i, line in enumerate(lines):
        counts[i] += 1
        matches = winning_matches(line)
        for j in range(1, matches+1):
            counts[i+j] += counts[i]
    return sum(counts)

print(part_one(data))
print(part_two(data))
