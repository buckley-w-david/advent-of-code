from aoc_utils import *
from aocd import get_data

data = get_data(year=2018, day=3, block=True)

import numpy as np

def parse_rectangles(data):
    lines = data.splitlines()
    return ([ (x, y, w, h) for _, x, y, w, h in map(ints, lines) ])

# I got tired trying to work out arbitrary overlapping rectangles algorithmically.
# I decided to just throw a bunch of memory at the problem and materialize all the rectangles into a huge numpy array

def part_one(data):
    rectangles = parse_rectangles(data)
    max_x, max_y = -1, -1

    for (x, y, w, h) in rectangles:
        max_x = max(x+w, max_x)
        max_y = max(y+h, max_y)

    field = np.zeros((max_y, max_x))

    for (x, y, w, h) in rectangles:
        field[y : y+h, x : x + w] += 1

    return (field > 1).sum()

def part_two(data):
    rectangles = parse_rectangles(data)
    max_x, max_y = -1, -1

    for (x, y, w, h) in rectangles:
        max_x = max(x+w, max_x)
        max_y = max(y+h, max_y)

    field = np.zeros((max_y, max_x))

    for (x, y, w, h) in rectangles:
        field[y : y+h, x : x + w] += 1

    for i, (x, y, w, h) in enumerate(rectangles):
        if np.all(field[y : y+h, x : x + w] == 1):
            return i+1

print(part_one(data))
print(part_two(data))
