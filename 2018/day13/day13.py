from enum import Enum, auto
from aoc_utils import *
from aocd import get_data

DIR = {
    '>': Direction.EAST.value,
    '<': Direction.WEST.value,
    'v': Direction.SOUTH.value,
    '^': Direction.NORTH.value,
}

class Turn(Enum):
    LEFT = auto()
    STRAIGHT = auto()
    RIGHT = auto()

TURNS = [Turn.LEFT, Turn.STRAIGHT, Turn.RIGHT]

def parse_carts(data):
    grid = [[c for c in l] for l in data.splitlines()]
    carts = {(y, x): (DIR[c], 0) for y, row in enumerate(grid) for x, c in enumerate(row) if c in { '<', '>', '^', 'v' }}

    return grid, carts


def part_one(data):
    grid, carts = parse_carts(data)

    while True:
        # pretty inefficient to keep sorting and resorting this
        # ... but meh, it works
        # I have commited far worse sins in this set of AoC
        ordered_carts = sorted(carts.keys())

        for y, x in ordered_carts:
            (dy, dx), t = carts.pop((y, x))
            ny, nx = y+dy, x+dx

            track = grid[ny][nx]
            if (ny, nx) in carts:
                return (nx, ny)
            elif track == '+':
                turn = TURNS[t]

                if turn is Turn.LEFT and dx == 0:
                    dy, dx = dx, dy
                elif turn is Turn.LEFT  and dy == 0:
                    dy, dx = -dx, -dy
                elif turn is Turn.STRAIGHT and dx == 0:
                    pass
                elif turn is Turn.STRAIGHT and dy == 0:
                    pass
                elif turn is Turn.RIGHT and dx == 0:
                    dy, dx = -dx, -dy
                elif turn is Turn.RIGHT and dy == 0:
                    dy, dx = dx, dy
                else:
                    assert False

                t = (t + 1) % len(TURNS)
            elif track == '\\':
                dy, dx = dx, dy
            elif track == '/':
                dy, dx = -dx, -dy

            carts[(ny, nx)] = ((dy, dx), t) # type: ignore

def part_two(data):
    grid, carts = parse_carts(data)

    while len(carts) != 1:
        ordered_carts = sorted(carts.keys())
        for (y, x) in ordered_carts:
            if (y, x) not in carts:
                continue

            (dy, dx), t = carts.pop((y, x))
            ny, nx = y+dy, x+dx

            track = grid[ny][nx]
            if (ny, nx) in carts:
                carts.pop((ny, nx))
                continue
            elif track == '+':
                turn = TURNS[t]

                if turn is Turn.LEFT and dx == 0:
                    dy, dx = dx, dy
                elif turn is Turn.LEFT and dy == 0:
                    dy, dx = -dx, dy
                elif turn is Turn.STRAIGHT:
                    pass
                elif turn is Turn.RIGHT and dx == 0:
                    dy, dx = dx, -dy
                elif turn is Turn.RIGHT and dy == 0:
                    dy, dx = dx, dy
                else:
                    assert False

                t = (t + 1) % len(TURNS)
            elif track == '\\':
                dy, dx = dx, dy
            elif track == '/':
                dy, dx = -dx, -dy

            carts[(ny, nx)] = ((dy, dx), t) # type: ignore

    (y, x), _ = carts.popitem()
    return (x, y)

data = get_data(year=2018, day=13, block=True)

print(part_one(data))
print(part_two(data))
