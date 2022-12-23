#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data


data = get_data(year=2022, day=23, block=True)
lines = data.splitlines()

elves = set()
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == '#':
            elves.add((y, x))

def around(p):
    y, x = p
    return {
        d: (y+d.value[0], x+d.value[1]) in elves for d in Direction
    }   

steps = [
    (Direction.NORTH, Direction.NE, Direction.NW, Direction.NORTH), 
    (Direction.SOUTH, Direction.SE, Direction.SW, Direction.SOUTH), 
    (Direction.WEST, Direction.NW, Direction.SW, Direction.WEST), 
    (Direction.EAST, Direction.NE, Direction.SE, Direction.EAST)
]

from collections import defaultdict
i = 0
while True:
    proposals = {}
    targets = defaultdict(int)
    next_round = set()
    for elf in elves:
        y, x = elf
        view = around(elf)
        dy, dx = 0, 0
        if not any(view.values()):
            target = (y+dy, x+dx)
            proposals[elf] = target
            targets[target] += 1
            continue
            
        for a, b, c, d in steps:
            if not (view[a] or view[b] or view[c]):
                dy, dx = d.value
                break

        target = (y+dy, x+dx)
        proposals[elf] = target
        targets[target] += 1

    for elf, p in proposals.items():
        if targets[p] > 1:
            next_round.add(elf)
            continue
        next_round.add(p) 
    assert len(elves) == len(next_round)
    i += 1
    if elves == next_round:
        print(i)
        break
    elves = next_round
    steps = steps[1:] + [steps[0]]

# Part 1
# min_x = min(elves, key=lambda p: p[1])[1]
# max_x = max(elves, key=lambda p: p[1])[1]

# min_y = min(elves, key=lambda p: p[0])[0]
# max_y = max(elves, key=lambda p: p[0])[0]

# empty = 0
# for y in range(min_y, max_y+1):
#     for x in range(min_x, max_x+1):
#         if (y, x) not in elves:
#             empty += 1
# print(empty)
