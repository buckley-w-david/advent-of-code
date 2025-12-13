from z3 import *

from aocd import get_data

data = get_data(year=2025, day=12, block=True)


def parse(data):
    shapes, regions = [], []
    *shapes_, regions_ = data.split("\n\n")

    for shape_ in shapes_:
        _, *lines = shape_.splitlines()
        shape = []
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "#":
                    shape.append((y, x))
        shapes.append(frozenset(shape))

    for region_ in regions_.splitlines():
        dims, counts = region_.split(": ")
        width, height = dims.split("x")
        counts = tuple(int(n) for n in counts.split(" "))
        regions.append(((int(width), int(height)), counts))

    return shapes, regions


# I am real mad that this works
def part_one(data):
    shapes, regions = parse(data)
    t = 0
    for (width, height), quantities in regions:
        total_area = width * height
        shape_area = sum(
            quantity * len(shape) for shape, quantity in zip(shapes, quantities)
        )

        if shape_area > total_area:
            # trivially impossible, there isn't enough space even if things were easy to arrange
            continue
        elif (width // 3) * (height // 3) >= sum(quantities):
            # trivially possible, you can just place everything in distinct 3x3 regions with no attempts to interleave them
            t += 1
        else:
            assert False

    return t


print(part_one(data))
