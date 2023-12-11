from itertools import accumulate, combinations
from typing import Iterable
from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=11, block=True)

def expansion_factor(grid: Grid, factor=2) -> tuple[list[int], list[int]]:
    empty_row = [True]*grid.height
    empty_column = [True]*grid.width

    for y in range(grid.height):
        for x in range(grid.width):
            empty_column[x] &= grid[y][x] == '.'
            empty_row[y] &= grid[y][x] == '.'

    return (
        [v*(factor-1) for v in accumulate(empty_row)],
        [v*(factor-1) for v in accumulate(empty_column)],
    )

def find_galaxies(grid: Grid) -> Iterable[tuple[int, int]]:
    for p, c in grid.row_major_with_index():
        if c == '#':
            yield p

def manhattan_distance(p1, p2):
    return abs(p2[1]-p1[1]) + abs(p2[0]-p1[0])

def solve(data, factor):
    grid = Grid([[c for c in l] for l in data.splitlines()])
    expand_y, expand_x = expansion_factor(grid, factor)

    s = 0
    for (g1, g2) in combinations(find_galaxies(grid), 2):
        p1 = g1[0]+expand_y[g1[0]], g1[1]+expand_x[g1[1]]
        p2 = g2[0]+expand_y[g2[0]], g2[1]+expand_x[g2[1]]
        s += manhattan_distance(p1, p2)

    return s

def part_one(data):
    return solve(data, 2)

def part_two(data):
    return solve(data, 1_000_000)

print(part_one(data))
print(part_two(data))
