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
