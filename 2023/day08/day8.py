import re
from math import lcm
from itertools import cycle

from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=8, block=True)
instructions, network = data.split("\n\n")

nodes = {}
for line in network.splitlines():
    m = re.match(r"(.*) = \((.*), (.*)\)", line)
    nodes[m.group(1)] = (m.group(2), m.group(3))


def part_one(instructions, nodes):
    current = 'AAA'
    steps = 0
    for ins in cycle(instructions):
        if ins == 'L':
            current = nodes[current][0]
        else:
            current = nodes[current][1]
        steps += 1
        if current == 'ZZZ':
            return steps

def part_two(instructions, nodes):
    current = [
        location for location in nodes if location.endswith('A')
    ]

    cycles = [0]*len(current)
    for i, c in enumerate(current):
        steps = 0
        for ins in cycle(instructions):
            if ins == 'L':
                c = nodes[c][0]
            else:
                c = nodes[c][1]
            steps += 1
            if c.endswith('Z'):
                cycles[i] = steps
                break

    return lcm(*cycles)

print(part_one(instructions, nodes))
print(part_two(instructions, nodes))
