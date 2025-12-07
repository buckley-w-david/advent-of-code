from collections import defaultdict
import enum
from functools import cache, reduce
from operator import mul
from aocd import get_data

from aoc_utils import Grid, Direction

data = get_data(year=2025, day=7, block=True)


class Cell(enum.Enum):
    EMPTY = enum.auto()
    SPLITTER = enum.auto()
    START = enum.auto()


def parse(data: str) -> tuple[Grid[Cell], tuple[int, int]]:
    def cast(c: str) -> Cell:
        if c == ".":
            return Cell.EMPTY
        elif c == "^":
            return Cell.SPLITTER
        else:
            return Cell.START

    grid: Grid[Cell] = Grid.parse(data, cast)
    for position, c in grid.row_major_with_index():
        if c is Cell.START:
            return grid, position
    assert False


def part_one(data):
    grid, start = parse(data)

    splitters = 0
    front = {start}
    while front:
        nf = set()
        for position in front:
            next_position = position + Direction.SOUTH
            if next_position not in grid:
                continue
            elif grid[next_position] is Cell.SPLITTER:
                splitters += 1
                left = next_position + Direction.EAST
                right = next_position + Direction.WEST
                if left in grid:
                    nf.add(left)
                if right in grid:
                    nf.add(right)
            else:
                nf.add(next_position)
        front = nf

    return splitters


def part_two(data):
    grid, start = parse(data)

    dependencies = defaultdict(set)
    exits = set()
    front = {(start, start)}
    while front:
        nf = set()
        for start, position in front:
            next_position = position + Direction.SOUTH
            if next_position not in grid:
                exits.add((position, start))
                continue
            elif grid[next_position] is Cell.SPLITTER:
                dependencies[next_position].add(start)
                left = next_position + Direction.EAST
                right = next_position + Direction.WEST
                if left in grid:
                    nf.add((next_position, left))
                if right in grid:
                    nf.add((next_position, right))
            else:
                nf.add((start, next_position))
        front = nf

    @cache
    def quantum_count(splitter):
        if not dependencies[splitter]:
            return 1

        return sum(quantum_count(s) for s in dependencies[splitter])

    return sum(quantum_count(splitter) for _, splitter in exits)


print(part_one(data))
print(part_two(data))
