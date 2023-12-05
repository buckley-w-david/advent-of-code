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

from collections import Counter
from aoc_utils import *
from aocd import get_data

data = get_data(year=2018, day=2, block=True)

def part_one(data):
    counts = [Counter(line) for line in data.splitlines()]
    twos = 0
    threes = 0
    for counter in counts:
        twos += 2 in counter.values()
        threes += 3 in counter.values()
    return twos * threes

# This is a terrible n*n*m (n=number of lines, m=length of line) algorithm
def part_two(data):
    lines = data.splitlines()
    for i, l1 in enumerate(lines):
        for l2 in lines[i+1:]:
            d = 0
            for j in range(len(l1)):
                d += l1[j] != l2[j]

            if d == 1:
                return ''.join(l1[i] for i in range(len(l1)) if l1[i] == l2[i])

print(part_one(data))
print(part_two(data))
