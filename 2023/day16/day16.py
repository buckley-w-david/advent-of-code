from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=16, block=True)
g = Grid([[c for c in l] for l in data.splitlines()])

def resolve(g, start=(0, 0, Direction.EAST)):
    history = set()
    beam_ends = {start}
    while True:
        next_beam_ends = set()
        for (y, x, dir) in beam_ends:
            dy, dx = dir.value
            history.add((y, x, dir))
            tile = g[(y, x)]
            if tile == '.':
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))
            elif tile == '/' and dir == Direction.NORTH:
                dir = Direction.EAST
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))
            elif tile == '/' and dir == Direction.EAST:
                dir = Direction.NORTH
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))
            elif tile == '/' and dir == Direction.SOUTH:
                dir = Direction.WEST
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))
            elif tile == '/' and dir == Direction.WEST:
                dir = Direction.SOUTH
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))
            elif tile == '\\' and dir == Direction.NORTH:
                dir = Direction.WEST
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))
            elif tile == '\\' and dir == Direction.EAST:
                dir = Direction.SOUTH
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))
            elif tile == '\\' and dir == Direction.SOUTH:
                dir = Direction.EAST
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))
            elif tile == '\\' and dir == Direction.WEST:
                dir = Direction.NORTH
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))
            elif tile == '-' and (dir == Direction.WEST or dir == Direction.EAST):
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))
            elif tile == '-' and (dir == Direction.NORTH or dir == Direction.SOUTH):
                dir = Direction.WEST
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))

                dir = Direction.EAST
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))
            elif tile == '|' and (dir == Direction.NORTH or dir == Direction.SOUTH):
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))
            elif tile == '|' and (dir == Direction.WEST or dir == Direction.EAST):
                dir = Direction.NORTH
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))

                dir = Direction.SOUTH
                dy, dx = dir.value
                if (y+dy, x+dx) in g:
                    next_beam_ends.add((y+dy, x+dx, dir))

        if not (next_beam_ends - history):
            break

        beam_ends = next_beam_ends

    energized = set()
    for (y, x, _) in history:
        energized.add((y, x))

    return len(energized)

def part_one(data):
    return resolve(g)

def part_two(data):
    g = Grid([[c for c in l] for l in data.splitlines()])
    me = -1
    for y in range(0, g.height):
        start = (y, 0, Direction.EAST)
        me = max(me, resolve(g, start))

    for y in range(0, g.height):
        start = (y, g.width-1, Direction.WEST)
        me = max(me, resolve(g, start))

    for x in range(0, g.width):
        start = (0, x, Direction.SOUTH)
        me = max(me, resolve(g, start))

    for x in range(0, g.width):
        start = (g.height-1, x, Direction.NORTH)
        me = max(me, resolve(g, start))

    return me

print(part_one(data))
print(part_two(data))
