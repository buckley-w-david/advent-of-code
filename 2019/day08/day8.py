#!/usr/bin/env python

from aocd import get_data
from aoc_utils import *

data = get_data(year=2019, day=8)
width = 25
height = 6

size = width*height

layers = [[int(c) for c in layer] for layer in chunk(data, size)]
image = [[2]*width for _ in range(height)]
for layer in layers:
    for i, c in enumerate(layer):
        y = i // width
        x = i % width
        if image[y][x] == 2:
            image[y][x] = c

for line in image:
    for c in line:
        if c == 2:
            print('x', end='')
        elif c == 1:
            print('#', end='')
        else:
            print(' ', end='')
    print()
