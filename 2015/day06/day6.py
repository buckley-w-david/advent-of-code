# Grid, Direction
# Direction.NORTH,SOUTH,EAST,WEST,NE,SE,NW,SW
# g = Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# g.width, g.height, (y, x) in g (coords), g[(y, x)], g[(y, x)] = 5
# for item in g => iterate over items in row major order
# g.row_major(_with_index)() => iterate over items in row major order
# g.column_major(_with_index)() => iterate over items in column major order
# g.apply(func) => call func with each item
# g.map(func) => return new Grid with results of func
# g.ray_from((y, x), direction), yields items from a starting point in a direction
# g.around(_with_index) => What it sounds like

# Graph
# g = Graph()
# g.add_edge(from, to, weight=something)
# g.dijkstra(start) => Dijkstra (has `distance_to`, and `path_to` methods)

# ShuntingYard
# Expression parser with configurable precedence for operations so you can throw out (B)EDMAS (no support for brackets)

import re

from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=6, block=True)


def part_one(data):
    state = [False] * 1_000_000
    for line in data.splitlines():
        m = re.match(r"(.*) (\d+),(\d+) through (\d+),(\d+)", line)
        instruction, x1, y1, x2, y2 = m.groups()
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                idx = y * 1_000 + x
                if instruction == "toggle":
                    state[idx] = not state[idx]
                elif instruction == "turn on":
                    state[idx] = True
                elif instruction == "turn off":
                    state[idx] = False
                else:
                    assert False
    return sum(state)


def part_two(data):
    state = [0] * 1_000_000
    for line in data.splitlines():
        m = re.match(r"(.*) (\d+),(\d+) through (\d+),(\d+)", line)
        instruction, x1, y1, x2, y2 = m.groups()
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                idx = y * 1_000 + x
                if instruction == "toggle":
                    state[idx] += 2
                elif instruction == "turn on":
                    state[idx] += 1
                elif instruction == "turn off":
                    state[idx] = max(state[idx] - 1, 0)
                else:
                    assert False
    return sum(state)


print(part_one(data))
print(part_two(data))
