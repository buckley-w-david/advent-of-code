#!/usr/bin/env python

from pprint import pprint
from aocd import get_data

data = get_data(year=2019, day=3, block=True)

vectors = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (1, 0),
    'D': (-1, 0),
}

directions = [direction.split(",") for direction in data.splitlines()]
wires = [{}, {}]
for i, wire in enumerate(directions):
    pos = (0, 0)
    s = 0
    for instr in wire:
        y, x = pos
        vy, vx = vectors[instr[0]]

        magnitude = int(instr[1:])
        if vx:
            for dx in range(1, magnitude+1):
                s += 1
                pos = (y, x+vx*dx)
                if pos not in wires[i]:
                    wires[i][pos] = s
        else:
            for dy in range(1, magnitude+1):
                s += 1
                pos = (y+vy*dy, x)
                if pos not in wires[i]:
                    wires[i][pos] = s
        pos = (y+vy*magnitude, x+vx*magnitude)

def distance(p):
    return sum(map(abs, p))

def steps(p):
    return wires[0][p] + wires[1][p]

intersections = set(wires[0].keys()).intersection(set(wires[1].keys())) - {(0, 0)}
pprint(steps(min(intersections, key=steps)))
