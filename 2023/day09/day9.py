from aoc_utils import *
from aocd import get_data

data = get_data(year=2023, day=9, block=True)

def parse_sequences(data):
    return [ints(line) for line in data.splitlines()]

def part_one(data):
    s = 0
    for sequence in parse_sequences(data):
        steps = [sequence]
        seq = sequence
        while not all(n == 0 for n in seq):
            seq = [seq[i+1]-seq[i] for i in range(0, len(seq)-1)]
            steps.append(seq)

        above = 0
        for step in reversed(steps[:-1]):
            above = step[-1] + above
        s += above
    return s

def part_two(data):
    s = 0
    for sequence in parse_sequences(data):
        steps = [sequence]
        seq = sequence
        while not all(n == 0 for n in seq):
            seq = [seq[i+1]-seq[i] for i in range(0, len(seq)-1)]
            steps.append(seq)

        above = 0
        for step in reversed(steps[:-1]):
            above = step[0] - above
        s += above
    return s

print(part_one(data))
print(part_two(data))
