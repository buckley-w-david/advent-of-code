#!/usr/bin/env python

from aocd import get_data, submit
from aoc_utils import Grid, Direction

from math import cos, sin
import math

data = get_data(year=2020, day=12, block=True)
# data = """
# F10
# N3
# F7
# R90
# F11
# """.strip()
instructions = [(l[0], int(l[1:])) for l in data.split("\n")]

dir = {
    'L': 1,
    'R': -1,
}
pos = [10, 1]
ship = [0, 0]

for instruction in instructions:
    command, value = instruction
    if command == "N":
        pos[1] += value
    elif command == "S":
        pos[1] -= value
    elif command == "E":
        pos[0] += value
    elif command == "W":
        pos[0] -= value
    elif command == "L" or command == "R":
        l = math.hypot(*pos)
        theta = math.degrees(math.atan2(pos[1], pos[0]))
        theta += dir[command]*value
        t_x = cos(math.radians(theta))
        t_y = sin(math.radians(theta))
        pos[0] = t_x*l
        pos[1] = t_y*l
    elif command == "F":
        dx = pos[0]
        dy = pos[1]
        ship[0] += value*dx
        ship[1] += value*dy


print(sum(map(round, map(abs, ship))))
