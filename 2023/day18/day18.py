import re
from aoc_utils import *
from aocd import get_data

def shoelace(points):
    t1 = points[-1][0]*points[0][1]
    t2 = points[-1][1]*points[0][0]
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        t1 += x1*y2
        t2 += y1*x2

    return abs(t1-t2)/2

RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)

direction_map = {
    "R": RIGHT,
    "D": DOWN,
    "L": LEFT,
    "U": UP,

    "0": RIGHT,
    "1": DOWN,
    "2": LEFT,
    "3": UP,
}

def parse_plan(data):
    dig_plan = []
    for line in data.splitlines():
        if match := re.match(r"(R|D|L|U) (\d+) \(#(.*)\)", line):
            d, count, colour = match.groups()
            direction = direction_map[d]

            dig_plan.append((direction, int(count), colour))
    return dig_plan


def part_one(data):
    dig_plan = parse_plan(data)

    location = (0, 0)
    vertices = [location]
    perimeter = 0
    for ((dx, dy), length, _) in dig_plan:
        x, y = location
        nx, ny = x + dx*length, y + dy*length
        location = (nx, ny)

        perimeter += abs(nx-x) + abs(ny-y)
        vertices.append(location)

    area = shoelace(vertices)
    return perimeter/2 + area + 1

def part_two(data):
    dig_plan = parse_plan(data)

    location = (0, 0)
    vertices = [location]
    perimeter = 0
    for ((dx, dy), length, colour) in dig_plan:
        length = int(colour[:5], 16)
        dx, dy = direction_map[colour[-1]]

        x, y = location
        nx, ny = x + dx*length, y + dy*length
        location = (nx, ny)

        perimeter += abs(nx-x) + abs(ny-y)
        vertices.append(location)

    area = shoelace(vertices)
    return perimeter/2 + area + 1


data = get_data(year=2023, day=18, block=True)

print(part_one(data))
print(part_two(data))
