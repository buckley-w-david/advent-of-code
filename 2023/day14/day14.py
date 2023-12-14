from typing import cast
from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=14, block=True)
platform = [list(line) for line in data.splitlines()]

def shift(platform, dir):
    dy, dx = dir
    height = len(platform)
    width = len(platform[0])

    left_y = 0
    right_y = len(platform)
    step_y = 1

    left_x = 0
    right_x = len(platform[0])
    step_x = 1

    if dir == (1, 0):
        left_y = len(platform)-1
        right_y = -1
        step_y = -1
    elif dir == (0, 1):
        left_x = len(platform[0])-1
        right_x = -1
        step_x = -1

    for y in range(left_y, right_y, step_y):
        for x in range(left_x, right_x, step_x):
            tile = platform[y][x]
            if tile == 'O':
                ty, tx = min(max(y+dy, 0), height-1), min(max(x+dx, 0), width-1)
                if platform[ty][tx] != '.':
                    continue
                while 0 <= ty+dy < height and 0 <= tx+dx < width and platform[ty+dy][tx+dx] == '.':
                    ty, tx = ty+dy, tx+dx
                platform[y][x] = '.'
                platform[ty][tx] = 'O'

def north_load(platform):
    height = len(platform)
    load = 0
    for y in range(len(platform)):
        for x in range(len(platform)):
            if platform[y][x] == 'O':
                load += height-y
    return load

def display(platform):
    for line in platform:
        print(''.join(line))


def raster(platform):
    return '\n'.join(''.join(line) for line in platform)


history = {}
for cycle in range(1_000_000_000):
    for d in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        shift(platform, d)
    r = raster(platform)
    if r in history:
        start = history[r]
        period = cycle - start
        skip = period * (1_000_000_000 // period) + start

        while skip > 1_000_000_000:
            skip -= period

        for cycle2 in range(skip+1, 1_000_000_000):
            for d in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                shift(platform, d)
        break
    else:
        history[r] = cycle

print(north_load(platform))
