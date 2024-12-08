from collections import defaultdict
from itertools import combinations

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=8, block=True)


def part_one(data):
    locations = defaultdict(set)
    grid = Grid([[c for c in line] for line in data.splitlines()])

    for yx, c in grid.row_major_with_index():
        if c != ".":
            locations[c].add(yx)

    antinodes = set()
    for _, positions in locations.items():
        for (ya, xa), (yb, xb) in combinations(sorted(positions), 2):
            dy = yb - ya
            dx = xb - xa

            p1 = (ya - dy, xa - dx)
            if p1 in grid:
                antinodes.add(p1)

            p2 = (yb + dy, xb + dx)
            if p2 in grid:
                antinodes.add(p2)

    return len(antinodes)


def part_two(data):
    locations = defaultdict(set)
    grid = Grid([[c for c in line] for line in data.splitlines()])

    for yx, c in grid.row_major_with_index():
        if c != ".":
            locations[c].add(yx)

    antinodes = set()
    for _, positions in locations.items():
        for (ya, xa), (yb, xb) in combinations(sorted(positions), 2):
            antinodes.add((ya, xa))
            antinodes.add((yb, xb))
            dy = yb - ya
            dx = xb - xa

            p1 = (ya - dy, xa - dx)
            while p1 in grid:
                antinodes.add(p1)
                p1 = (p1[0] - dy, p1[1] - dx)

            p2 = (yb + dy, xb + dx)
            while p2 in grid:
                antinodes.add(p2)
                p2 = (p2[0] + dy, p2[1] + dx)

    return len(antinodes)


print(part_one(data))
print(part_two(data))
