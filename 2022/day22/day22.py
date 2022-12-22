#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data


data = get_data(year=2022, day=22, block=True)

map, path = data.split("\n\n")
ml = map.splitlines()

WALL = 1
PATH = 0
INVALID = -1
width = max(len(r) for r in ml)
coords = []
for y in range(len(ml)):
    row = []
    r = ml[y]
    for x in range(width):
        if x >= len(ml[y]):
            row.append(INVALID)
        elif ml[y][x] == '.':
            row.append(PATH)
        elif ml[y][x] == '#':
            row.append(WALL)
        else:
            row.append(INVALID)
    coords.append(row)
grid = Grid(coords)

SQUARE_SIZE = 50

dir = Direction.EAST
rotate = {
    (Direction.EAST, 'L'): Direction.NORTH,
    (Direction.NORTH, 'L'): Direction.WEST,
    (Direction.WEST, 'L'): Direction.SOUTH,
    (Direction.SOUTH, 'L'): Direction.EAST,
    (Direction.EAST, 'R'): Direction.SOUTH,
    (Direction.SOUTH, 'R'): Direction.WEST,
    (Direction.WEST, 'R'): Direction.NORTH,
    (Direction.NORTH, 'R'): Direction.EAST,
}
num = {
    Direction.EAST: 0,
    Direction.SOUTH: 1,
    Direction.WEST: 2,
    Direction.NORTH: 3,
}
import re

ONE = 0, 2 
TWO = 0, 1
THREE = 1, 1
FOUR = 2, 1
FIVE = 2, 0
SIX = 3, 0

ranges = {
    ONE: (ONE[0]*SQUARE_SIZE, ONE[1]*SQUARE_SIZE),
    TWO: (TWO[0]*SQUARE_SIZE, TWO[1]*SQUARE_SIZE),
    THREE: (THREE[0]*SQUARE_SIZE, THREE[1]*SQUARE_SIZE),
    FOUR: (FOUR[0]*SQUARE_SIZE, FOUR[1]*SQUARE_SIZE),
    FIVE: (FIVE[0]*SQUARE_SIZE, FIVE[1]*SQUARE_SIZE),
    SIX: (SIX[0]*SQUARE_SIZE, SIX[1]*SQUARE_SIZE),
}

translations = {
    ONE: {
        Direction.EAST: (FOUR, Direction.WEST),
        Direction.WEST: (TWO, Direction.WEST),
        Direction.NORTH: (SIX, Direction.NORTH),
        Direction.SOUTH: (THREE, Direction.WEST),
    },
    TWO: {
        Direction.EAST: (ONE, Direction.EAST),
        Direction.WEST: (FIVE, Direction.EAST),
        Direction.NORTH: (SIX, Direction.EAST),
        Direction.SOUTH: (THREE, Direction.SOUTH),
    },
    THREE: {
        Direction.EAST: (ONE, Direction.NORTH),
        Direction.WEST: (FIVE, Direction.SOUTH),
        Direction.NORTH: (TWO, Direction.NORTH),
        Direction.SOUTH: (FOUR, Direction.SOUTH),
    },
    FOUR: {
        Direction.EAST: (ONE, Direction.WEST),
        Direction.WEST: (FIVE, Direction.WEST),
        Direction.NORTH: (THREE, Direction.NORTH),
        Direction.SOUTH: (SIX, Direction.WEST),
    },
    FIVE: {
        Direction.EAST: (FOUR, Direction.EAST),
        Direction.WEST: (TWO, Direction.EAST),
        Direction.NORTH: (THREE, Direction.EAST),
        Direction.SOUTH: (SIX, Direction.SOUTH),
    },
    SIX: {
        Direction.EAST: (FOUR, Direction.NORTH),
        Direction.WEST: (TWO, Direction.SOUTH),
        Direction.NORTH: (FIVE, Direction.NORTH),
        Direction.SOUTH: (ONE, Direction.SOUTH),
    },
}

heading = {}
y, x = 0, ml[0].index('.')
dir = Direction.EAST
face = TWO
for instruction in re.findall(r"(\d+|[LR])", path):
    if instruction == 'L' or instruction == 'R':
        dir = rotate[(dir, instruction)] # type: ignore
        heading[y, x] = dir
        continue
    l = int(instruction)
    for _ in range(l):
        face = y // SQUARE_SIZE, x // SQUARE_SIZE
        start_y, start_x = ranges[face] # type: ignore
        end_y, end_x = start_y+SQUARE_SIZE, start_x+SQUARE_SIZE

        heading[(y, x)] = dir
        if dir == Direction.EAST:
            cy, cx = y, x+1
        elif dir == Direction.WEST:
            cy, cx = y, x-1
        elif dir == Direction.SOUTH:
            cy, cx = y+1, x
        else:
            cy, cx = y-1, x
        nf, nd = face, dir
        if not (start_x <= cx < end_x and start_y <= cy < end_y):
            nf, nd = translations[face][dir] # type: ignore
            ry, rx = cy % SQUARE_SIZE, cx % SQUARE_SIZE
            by, bx = ranges[nf]
            # Yuck
            if dir == Direction.EAST and nd == Direction.NORTH:
                cy, cx = by + SQUARE_SIZE-1, bx + ry
            elif dir == Direction.EAST and nd == Direction.SOUTH:
                assert False
            elif dir == Direction.EAST and nd == Direction.WEST:
                # invert Y
                cy, cx = by + SQUARE_SIZE-1 - ry, bx + SQUARE_SIZE-1
            elif dir == Direction.WEST and nd == Direction.NORTH:
                assert False
            elif dir == Direction.WEST and nd == Direction.SOUTH:
                cy, cx = by, bx + ry
            elif dir == Direction.WEST and nd == Direction.EAST:
                cy, cx = by + SQUARE_SIZE-1 - ry, bx
            elif dir == Direction.NORTH and nd == Direction.EAST:
                cy, cx = by + rx, bx
            elif dir == Direction.NORTH and nd == Direction.WEST:
                assert False
            elif dir == Direction.NORTH and nd == Direction.SOUTH:
                assert False
            elif dir == Direction.SOUTH and nd == Direction.EAST:
                assert False
            elif dir == Direction.SOUTH and nd == Direction.WEST:
                # Swap
                cy, cx = by + rx, bx + SQUARE_SIZE-1
            elif dir == Direction.SOUTH and nd == Direction.NORTH:
                assert False
            else:
                cy, cx = by + ry, bx + rx
        if grid[cy, cx] == WALL:
            break
        y, x, face, dir = cy, cx, nf, nd

print(1000*(y+1)+4*(x+1)+num[dir])
