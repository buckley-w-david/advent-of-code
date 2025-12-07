from collections import defaultdict

from aocd import get_data

from aoc_utils import Grid, Direction

data = get_data(year=2025, day=7, block=True)


def parse(data: str) -> tuple[Grid[str], tuple[int, int]]:
    grid = Grid.parse(data)
    for position, c in grid.row_major_with_index():
        if c == "S":
            return grid, position
    assert False


def part_one(data):
    grid, start = parse(data)

    splitters = 0
    front = {start}

    # Each step moves us down one row
    # As such, we only have to advance down to the last row (which has no splitters)
    for _ in range(grid.height - 1):
        nf = set()

        for position in front:
            next_position = position + Direction.SOUTH
            if grid[next_position] == "^":
                splitters += 1

                nf.add(next_position + Direction.EAST)
                nf.add(next_position + Direction.WEST)
            else:
                nf.add(next_position)

        front = nf

    return splitters


def part_two(data):
    grid, start = parse(data)

    front = {(start, start)}
    counts = defaultdict(int)
    counts[start] = 1

    for _ in range(grid.height - 1):
        nf = set()

        for source, position in front:
            next_position = position + Direction.SOUTH
            if grid[next_position] == "^":
                counts[next_position] += counts[source]

                nf.add((next_position, next_position + Direction.EAST))
                nf.add((next_position, next_position + Direction.WEST))
            else:
                nf.add((source, next_position))

        front = nf

    return sum(counts.values())


print(part_one(data))
print(part_two(data))
