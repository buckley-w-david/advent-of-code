from aoc_utils import * # type: ignore
from aocd import get_data

def parse_grid(data):
    return [[c for c in line] for line in data.splitlines()]

def around(grid, p):
    height = width = len(grid)
    y, x = p
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) == abs(j):
                continue
            ny, nx = (y + i, x + j)
            yield (ny, nx), grid[ny % height][nx % width]

def part_one(data):
    grid = parse_grid(data)
    width = height = len(grid)

    stepped = set()
    for y in range(height):
        for x in range(width):
            p = (y, x)
            t = grid[y][x]
            if t == 'S':
                stepped.add(p)
                break

    for _ in range(64):
        next_step = set()
        for point in stepped:
            for p, t in around(grid, point):
                if t == '#': continue
                next_step.add(p)
        stepped = next_step

    return len(stepped)

def part_two(data):
    grid = parse_grid(data)
    width = height = len(grid)
    stepped = set()

    for y in range(height):
        for x in range(width):
            p = (y, x)
            t = grid[y][x]
            if t == 'S':
                stepped.add(p)
                break

    # Fill out a 5x5 set of maps
    for _ in range(2*width + width // 2):
        next_step = set()
        for point in stepped:
            for p, t in around(grid, point):
                if t == '#': continue
                next_step.add(p)
        stepped = next_step

    # This map has all the components of our full one
    shapes = [
        ( (0, 1), (-2, -1) ),  # left cone
        ( (0, 1), (2, 3) ),    # right cone
        ( (-2, -1), (0, 1) ),  # top cone
        ( (2, 3), (0, 1) ),    # bottom cone

        ( (-2, -1), (-1, 0) ), # top left corner
        ( (-2, -1), (1, 2) ),  # top right corner
        ( (2, 3), (-1, 0) ),   # bottom left corner
        ( (2, 3), (1, 2) ),    # bottom right corner

        ( (-1, 0), (-1, 0) ),  # top left anti-corner
        ( (-1, 0), (1, 2) ),   # top right anti-corner
        ( (1, 2), (-1, 0) ),   # bottom left anti-corner
        ( (1, 2), (1, 2) ),    # bottom right anti-corner

        ( (0, 1), (0, 1) ),    # type-1 full
        ( (1, 2), (0, 1) ),    # type-2 full
    ]

    # The total number of plots will be multiples of the counts of our 5x5 versions
    counts = [0]*len(shapes)
    for i, ( (y0, y1), (x0, x1) ) in enumerate(shapes):
        for y in range(y0*height, y1*height):
            for x in range(x0*height, x1*height):
                counts[i] += (y, x) in stepped

    steps = 26501365

    # The number of squares from the middle to the edge
    length = (steps - width//2) // width

    # cones + length*corner + (length-1)*anti_corner
    edge_steps = sum(counts[:4]) + sum(n*length for n in counts[4:8]) + sum(n*(length - 1) for n in counts[8:12])

    # The interior maps have two versions depending on parity
    interior_steps_1 = counts[13] * ( length*(length-1) + length )
    interior_steps_2 = counts[12] * ( (length-1)*(length-2) + (length-1) )

    return edge_steps + interior_steps_1 + interior_steps_2

data = get_data(year=2023, day=21, block=True)

print(part_one(data))
print(part_two(data))
