from itertools import accumulate, combinations
from typing import Iterable
from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=11, block=True)

def print_grid(grid: Grid):
    for y in range(grid.height):
        for x in range(grid.width):
            print(end=grid[y][x])
        print()

def expansion_factor(grid: Grid) -> tuple[list[bool], list[bool]]:
    empty_row = [True]*grid.height
    empty_column = [True]*grid.width

    for y in range(grid.height):
        for x in range(grid.width):
            empty_column[x] &= grid[y][x] == '.'
            empty_row[y] &= grid[y][x] == '.'

    return list(accumulate(empty_row)), list(accumulate(empty_column))

def find_galaxies(grid: Grid) -> Iterable[tuple[int, int]]:
    for p, c in grid.row_major_with_index():
        if c == '#':
            yield p

def manhattan_distance(p1, p2):
    return abs(p2[1]-p1[1]) + abs(p2[0]-p1[0])

def part_one(data):
    grid = Grid([[c for c in l] for l in data.splitlines()])
    expand_y, expand_x = expansion_factor(grid)

    s = 0
    for (g1, g2) in combinations(find_galaxies(grid), 2):
        p1 = g1[0]+expand_y[g1[0]], g1[1]+expand_x[g1[1]]
        p2 = g2[0]+expand_y[g2[0]], g2[1]+expand_x[g2[1]]
        s += manhattan_distance(p1, p2)

    return s

def part_two(data):
    grid = Grid([[c for c in l] for l in data.splitlines()])
    expand_y, expand_x = expansion_factor(grid)
    factor = 1000000

    expand_y = [v*(factor-1) for v in expand_y]
    expand_x = [v*(factor-1) for v in expand_x]

    s = 0
    for (g1, g2) in combinations(find_galaxies(grid), 2):
        p1 = g1[0]+expand_y[g1[0]], g1[1]+expand_x[g1[1]]
        p2 = g2[0]+expand_y[g2[0]], g2[1]+expand_x[g2[1]]
        s += manhattan_distance(p1, p2)
    return s

print(part_one(data))
print(part_two(data))
