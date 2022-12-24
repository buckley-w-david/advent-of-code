#!/usr/bin/env python

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
# from aoc_utils import * # type: ignore

# from aocd import get_data

import enum

class Direction(enum.Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)
    NE = (-1, 1)
    SE = (1, 1)
    NW = (-1, -1)
    SW = (1, -1)


# data = get_data(year=2022, day=24, block=True)
with open('input.txt', 'r') as f:
    data = f.read()
#data = """#.######
##>>.<^<#
##.<..<<#
##>v.><>#
##<^v^^>#
#######.#"""
lines = data.splitlines()

tiles = {
    '.': 0,
    '#': 1,
    '>': 2,
    '<': 3,
    '^': 4,
    'v': 5,
}
field = []
walls = set()
blizzards = set()
width = len(lines[0])
height = len(lines)
start = (0, lines[0].index('.'))
target = (height-1, lines[-1].index('.'))
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == '#':
            walls.add((y, x))
        elif c == '>':
            blizzards.add(((y, x), Direction.EAST))
        elif c == '<':
            blizzards.add(((y, x), Direction.WEST))
        elif c == '^':
            blizzards.add(((y, x), Direction.NORTH))
        elif c == 'v':
            blizzards.add(((y, x), Direction.SOUTH))

def bliz_pos(blizzard, g):
    ((y, x), d) = blizzard
    dy, dx = d.value
    return ((y - 1 + dy*g) % (height-2)) + 1, ((x - 1 + dx*g) % (width-2)) + 1

from functools import cache

@cache
def blocked(generation):
    return frozenset( bliz_pos(b, generation) for b in blizzards )

fastest = float('inf')
def neighbours(state):
    p, generation = state
    if p == target or generation > fastest:
        return []

    y, x = p
    no_go = blocked(generation)

    for d in [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]:
        dy, dx = d.value
        cy, cx = y+dy, x+dx
        candidate = (cy, cx)
        if 0 <= cy < height and 0 <= cx < width and candidate not in walls and candidate not in no_go:
            yield candidate, generation+1
    if p not in no_go:
        yield p, generation+1

from collections import deque
history = set([(start, 1)])
queue = deque([(start, 1)])


while queue:
    state = queue.pop()
    if state[0] == target and state[1] < fastest:
        print('reached', target, 'in', state[1]-1)
        fastest = state[1]

    for other_node in neighbours(state):
        if other_node not in history:
            history.add(other_node)
            queue.appendleft(other_node)

start, target = target, start

history = set([(start, fastest)])
queue = deque([(start, fastest)])
fastest = float('inf')

while queue:
    state = queue.pop()
    if state[0] == target and state[1] < fastest:
        print('reached', target, 'in', state[1]-1)
        fastest = state[1]

    for other_node in neighbours(state):
        if other_node not in history:
            # print(state[1])
            # display(other_node[0], state[1])
            # breakpoint()
            history.add(other_node)
            queue.appendleft(other_node)

start, target = target, start
history = set([(start, fastest)])
queue = deque([(start, fastest)])
fastest = float('inf')

while queue:
    state = queue.pop()
    if state[0] == target and state[1] < fastest:
        print('reached', target, 'in', state[1]-1)
        fastest = state[1]

    for other_node in neighbours(state):
        if other_node not in history:
            # print(state[1])
            # display(other_node[0], state[1])
            # breakpoint()
            history.add(other_node)
            queue.appendleft(other_node)
