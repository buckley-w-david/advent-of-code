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

from io import StringIO
from aoc_utils import *
from aocd import get_data

data = get_data(year=2018, day=10, block=True)

lights = {
    tuple(ints(line)) for line in data.splitlines()
}

def raster(lights):
    minx, maxx, miny, maxy = float('inf'), -float('inf'), float('inf'), -float('inf')
    for x, y  in lights:
        minx = min(x, minx)
        maxx = max(x, maxx)
        miny = min(y, miny)
        maxy = max(y, maxy)

    if maxx - minx > 1_000:
        return None
    elif maxy - miny > 1_000:
        return None

    sio = StringIO()
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (x, y) in lights:
                sio.write("#")
            else:
                sio.write(" ")
        sio.write("\n")
    return sio.getvalue()

def check(args):
    lights, steps = args
    new_lights = { (x+dx*steps, y+dy*steps) for (x, y, dx, dy) in lights }
    s = raster(new_lights)
    return s

def compute(lights, steps):
    return frozenset((x+dx*steps, y+dy*steps) for (x, y, dx, dy) in lights)

# Found through generating many candidates and visually inspecting them
correct_lights = compute(lights, 10_009)
