from collections import defaultdict
import re
from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=3, block=True)
lines = data.splitlines()

def part_one(lines):
    part_numbers = []
    g = Grid([[c for c in line] for line in lines])
    for y, line in enumerate(lines):
        for m in re.finditer(r"(\d+)", line):
            start, end = m.span()
            n = int(m.group(1))
            adj_symbol = False
            for x in range(start, end):
                pc = (y, x)
                for _, c in g.around_with_index(pc):
                    if not (c.isdigit() or c == '.'):
                        adj_symbol = True
                        break
                if adj_symbol:
                    break
            if adj_symbol:
                part_numbers.append(n)

    return sum(part_numbers)

def part_two(lines):
    g = Grid([[c for c in line] for line in lines])

    numbers = defaultdict(dict)
    for y, line in enumerate(lines):
        for m in re.finditer(r"(\d+)", line):
            numbers[y][m.span()] = int(m.group(1))

    stars = set()
    for p, c in g.row_major_with_index():
        if c == '*':
            stars.add(p)

    s = 0
    for p in stars:
        adj = set()
        for (y, x), _ in g.around_with_index(p):
            for (sx, ex) in numbers[y]:
                if sx <= x < ex:
                    adj.add((y, (sx, ex)))
        if len(adj) == 2:
            prod = 1
            for (y, span) in adj:
                prod *= numbers[y][span]
            s += prod
    return s

print(part_one(lines))
print(part_two(lines))
