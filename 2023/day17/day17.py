from aoc_utils import * # type: ignore
from aocd import get_data
from typing import cast

EAST = (1, 0)
WEST = (-1, 0)
NORTH = (0, -1)
SOUTH = (0, 1)

data = get_data(year=2023, day=17, block=True)
grid = Grid([[int(c) for c in l] for l in data.splitlines()])

# d = direction
# s = streak
#        y  x  d     s
start = (0, 0, EAST, 0)
target = (grid.height-1, grid.width-1)

def crucible_neighbours(p):
    y, x, direction, streak = p
    dx, dy = direction
    prev_y, prev_x = y-dy, x-dx

    transitions = []

    if p == start:
        transitions.append((1, 0, SOUTH, 1))
        transitions.append((0, 1, EAST, 1))
    elif direction == NORTH or direction == SOUTH:
        transitions.append((y, x+1, EAST, 1))
        transitions.append((y, x-1, WEST, 1))
    else:
        transitions.append((y+1, x, SOUTH, 1))
        transitions.append((y-1, x, NORTH, 1))

    if 1 <= streak < 3:
        transitions.append((y+dy, x+dx, direction, streak+1))

    for point in transitions:
        (py, px, _, _) = point
        if (py, px) == (prev_y, prev_x):
            continue
        if (py, px) not in grid:
            continue

        cost = cast(int, grid[py, px])
        yield (cost, point)

def ultra_crucible_neighbours(p):
    y, x, direction, streak = p
    dx, dy = direction
    prev_y, prev_x = y-dy, x-dx

    transitions = []

    if p == start:
        transitions.append((1, 0, SOUTH, 1))
        transitions.append((0, 1, EAST, 1))

    if streak >= 4:
        if direction == NORTH or direction == SOUTH:
            transitions.append((y, x+1, EAST, 1))
            transitions.append((y, x-1, WEST, 1))
        else:
            transitions.append((y+1, x, SOUTH, 1))
            transitions.append((y-1, x, NORTH, 1))

    if 1 <= streak < 10:
        transitions.append((y+dy, x+dx, direction, streak+1))

    for point in transitions:
        (py, px, _, next_streak) = point
        if (py, px) == target and next_streak < 4:
            continue
        if (py, px) == (prev_y, prev_x):
            continue
        if (py, px) not in grid:
            continue

        cost = cast(int, grid[py, px])
        yield (cost, point)

def solve(neighbour_fn):
    graph = LazyGraph(neighbour_fn)
    d = graph.dijkstra(start)
    md = float('inf')

    # Technically the "target" is actually many different potential points
    # one set of x and y, but a wide range of direction and streak values
    # this we have to find all the "targets" and check which of them is the best
    for (y, x, _, _), distance in d.distances.items():
        if (y, x) == target:
            if distance <= md:
                md = distance

    return md


def part_one():
    return solve(crucible_neighbours)

def part_two():
    return solve(ultra_crucible_neighbours)

print(part_one())
print(part_two())
