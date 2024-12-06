import re

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=6, block=True)


def parse(data):
    grid = Grid([[c for c in line] for line in data.splitlines()])
    guard = None

    for yx, c in grid.row_major_with_index():
        if c == "^":
            guard = yx
            break
    grid[guard] = "."
    return grid, guard


def simulate(grid, guard):
    direction = Direction.NORTH
    visited = set([(guard, direction)])

    while True:
        y, x = guard
        dy, dx = direction.value
        yy, xx = y + dy, x + dx

        yyxx = (yy, xx)

        if yyxx not in grid:
            return visited

        if (yyxx, direction) in visited:
            return None

        if grid[yyxx] != ".":
            direction = direction.rotate(cardinal=True)
        else:
            guard = yyxx
            visited.add((yyxx, direction))


def part_one(data):
    grid, starting = parse(data)
    visited = set(p for p, _ in simulate(grid, starting))
    return len(visited)


def part_two(data):
    grid, starting = parse(data)

    visited = simulate(grid, starting)

    assert visited

    looped = 0
    tried = set()
    for yx, _ in visited:
        for yx, _ in grid.around_with_index(yx, corners=False):
            if yx in tried:
                continue

            tried.add(yx)

            if grid[yx] != "." or yx == starting:
                continue

            grid[yx] = "#"

            visited = simulate(grid, starting)

            grid[yx] = "."

            if visited is None:
                looped += 1

    return looped


print(part_one(data))
print(part_two(data))
