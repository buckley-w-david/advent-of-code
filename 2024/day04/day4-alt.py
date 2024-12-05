from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=4, block=True)


def pattern_search(grid, patterns, words):
    w = next(iter(words))
    assert all(len(word) == len(w) for word in words)
    assert all(len(p) == len(w) for p in patterns)

    taken = set()

    for (y, x), _ in grid.row_major_with_index():
        for pattern in patterns:
            stamp = [(y + dy, x + dx) for (dy, dx) in pattern]
            string = "".join(grid[y][x] for y, x in stamp if (y, x) in grid)

            if string in words:
                taken.add(tuple(sorted(stamp)))

    return taken


def part_one(data):
    patterns = [
        ((0, 0), (0, 1), (0, 2), (0, 3)),
        ((0, 0), (0, -1), (0, -2), (0, -3)),
        ((0, 0), (1, 0), (2, 0), (3, 0)),
        ((0, 0), (-1, 0), (-2, 0), (-3, 0)),
        ((0, 0), (1, 1), (2, 2), (3, 3)),
        ((0, 0), (-1, -1), (-2, -2), (-3, -3)),
        ((0, 0), (1, -1), (2, -2), (3, -3)),
        ((0, 0), (-1, 1), (-2, 2), (-3, 3)),
    ]
    grid = Grid([[c for c in line] for line in data.splitlines()])

    return len(pattern_search(grid, patterns, ["XMAS"]))


def part_two(data):
    patterns = [
        ((0, 0), (0, 2), (1, 1), (2, 0), (2, 2)),
    ]
    words = {"MSAMS", "SMASM", "MMASS", "SSAMM"}
    grid = Grid([[c for c in line] for line in data.splitlines()])

    return len(pattern_search(grid, patterns, words))


print(part_one(data))
print(part_two(data))
