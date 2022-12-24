#!/usr/bin/env python

from functools import cache

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2022, day=24, block=True)
lines = data.splitlines()

walls = set()
blizzards = set()
width = len(lines[0])
height = len(lines)
start = (0, lines[0].index("."))
target = (height - 1, lines[-1].index("."))
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        p = (y, x)
        if c == "#":
            walls.add(p)
        elif c == ">":
            blizzards.add((p, Direction.EAST))
        elif c == "<":
            blizzards.add((p, Direction.WEST))
        elif c == "^":
            blizzards.add((p, Direction.NORTH))
        elif c == "v":
            blizzards.add((p, Direction.SOUTH))


def bliz_pos(blizzard, gen):
    ((y, x), d) = blizzard
    dy, dx = d.value
    return ((y - 1 + dy * gen) % (height - 2)) + 1, ((x - 1 + dx * gen) % (width - 2)) + 1


@cache
def blocked(gen):
    return frozenset(bliz_pos(b, gen) for b in blizzards)


def neighbours(state):
    p, generation = state
    if p == target or generation > fastest:
        return []

    y, x = p
    no_go = blocked(generation)

    for d in [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]:
        dy, dx = d.value
        cy, cx = y + dy, x + dx
        candidate = (cy, cx)
        if (
            0 <= cy < height
            and 0 <= cx < width
            and candidate not in walls
            and candidate not in no_go
        ):
            yield candidate, generation + 1

    if p not in no_go:
        yield p, generation + 1


def visit(state):
    global fastest, target

    p, gen = state
    if p == target and gen < fastest:
        fastest = gen

    return True


graph = UnweightedLazyGraph(neighbours)
gen = 1
fastest = float("inf")
for _ in range(3):
    fastest = float("inf")
    graph.bfs((start, gen), visit)
    start, target = target, start
    gen = fastest
print(fastest)
