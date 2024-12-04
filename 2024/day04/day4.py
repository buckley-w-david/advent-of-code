from itertools import islice, combinations

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=4, block=True)


def word_search(grid, word):
    taken = set()
    reverse = "".join(reversed(word))
    ray_length = len(word) - 1

    for yx, c in grid.row_major_with_index():
        for d in Direction:
            ray = islice(grid.ray_from_with_index(yx, d), ray_length)
            chars = [c]
            pos = [yx]

            for yyx, cc in ray:
                pos.append(yyx)
                chars.append(cc)

            string = "".join(chars)
            if string == word or string == reverse:
                taken.add(tuple(sorted(pos)))

    return taken


def part_one(data):
    grid = Grid([[c for c in line] for line in data.splitlines()])

    return len(word_search(grid, "XMAS"))


def part_two(data):
    grid = Grid([[c for c in line] for line in data.splitlines()])
    occurances = word_search(grid, "MAS")

    xmases = 0
    for first, second in combinations(occurances, 2):
        m1, a1, s1 = first
        m2, a2, s2 = second

        if (
            m1[0] == m2[0]
            and abs(m1[1] - m2[1]) == 2
            and a1 == a2
            and s1[0] == s2[0]
            and abs(s1[1] - s2[1]) == 2
        ):
            xmases += 1
    return xmases


print(part_one(data))
print(part_two(data))
