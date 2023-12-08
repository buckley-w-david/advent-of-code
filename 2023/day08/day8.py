import re
from math import lcm
from itertools import cycle

from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=8, block=True)

def parse_map(data):
    ins, network = data.split("\n\n")

    instructions = [0 if i == 'L' else 1 for i in ins]

    nodes = {}
    for line in network.splitlines():
        m = re.match(r"(.*) = \((.*), (.*)\)", line)
        nodes[m.group(1)] = (m.group(2), m.group(3))

    return instructions, nodes

def part_one(data):
    instructions, nodes = parse_map(data)
    current = 'AAA'
    steps = 0
    for ins in cycle(instructions):
        current = nodes[current][ins]
        steps += 1
        if current == 'ZZZ':
            return steps

def part_two(data):
    instructions, nodes = parse_map(data)
    current = [
        location for location in nodes if location.endswith('A')
    ]

    cycles = [0]*len(current)
    for i, c in enumerate(current):
        steps = 0
        for ins in cycle(instructions):
            c = nodes[c][ins]
            steps += 1
            if c.endswith('Z'):
                cycles[i] = steps
                break

    return lcm(*cycles)

print(part_one(data))
print(part_two(data))
