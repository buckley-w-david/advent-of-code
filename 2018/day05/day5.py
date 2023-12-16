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

import string
import re
from aoc_utils import *
from aocd import get_data

data = get_data(year=2018, day=5, block=True)

def part_one(data):
    polymer = list(data)
    new_polymer = []
    i = 0

    while True:
        while i < len(polymer)-1:
            u1, u2 = polymer[i], polymer[i+1]
            if u1.islower() and u2.isupper() and u1 == u2.lower() or \
               u2.islower() and u1.isupper() and u2 == u1.lower():
                i += 1
            else:
                new_polymer.append(u1)
            i += 1
        if i != len(polymer):
            new_polymer.append(polymer[-1])

        if polymer == new_polymer:
            return len(polymer)

        polymer = new_polymer
        new_polymer = []
        i = 0

# Lazy brute force method
# part_one is slow (3 seconds), and this is even slower (~35 seconds)
# but it works
def part_two(data):
    l = float('inf')
    for letter in string.ascii_lowercase:
        l = min(l, part_one(data.replace(letter, '').replace(letter.upper(), '')))
    return l

print(part_one(data))
print(part_two(data))
