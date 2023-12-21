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

from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=21, block=True)
# data = """...........
# .....###.#.
# .###.##..#.
# ..#.#...#..
# ....#.#....
# .##..S####.
# .##..#...#.
# .......##..
# .##.#.####.
# .##..##.##.
# ..........."""
grid = Grid([[c for c in line] for line in data.splitlines()])
graph = Graph()

stepped = set()

for p, t in grid.row_major_with_index():
    if t == 'S':
        stepped.add(p)
        break

def around(p):
    y, x = p
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) == abs(j):
                continue
            ny, nx = (y + i, x + j)
            yield (ny, nx), grid[ny % grid.height, nx % grid.width]

STEPS = grid.width
for _ in range(STEPS):
    next_step = set()
    for point in stepped:
        for p, t in around(point):
            if t == '#': continue
            next_step.add(p)
    stepped = next_step

"""
26501365 steps means the spread is 26501365 in all 4 cardinal directions
The direction vertical and horizontal trajectories are clear, so it can spread unimpeded

The board is 131x131
26501365 / 131 = 202300.4961832061
that means we will have covered ~202300 boards of distance

It isn't very difficult to work out if most coordinates will be in the visitable set after n steps via simple calculation (alternating even and odd step counts)
The difficult thing is going to be the edges. They are not perfectly smooth and their exact configuration depends on how far into the tile we are.
I think I'm going to have to generate all "versions" of a filling tile there are, scan the edge of the pattern, and figure out which version it maps to.
Then I can do calc(most of the shape) + mapping[edges]

I think I should be able to generate the versions from a 3x3 set of tiles
"""

for y in range(-grid.height*2, grid.height*2):
    for x in range(-grid.width*2, grid.width*2):
        if (y, x) in stepped:
            print(end='O')
        else:
            print(end=grid[(y % grid.height, x % grid.width)])
    print()

