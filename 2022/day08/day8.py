#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

data = get_data(year=2022, day=8, block=True)

l = map(list, data.splitlines())
l = [list(map(int, l)) for l in l]
g = Grid(l)

# Part 1 code
# visible = set()
# for x in range(g.width):
#     visible.add((0, x))
#     m = g[(0, x)]
#     for point, elem in g.ray_from_with_index((0, x), Direction.SOUTH):
#         if elem > m:
#             visible.add(point)
#             m = elem
#     visible.add((g.height-1, x))
#     m = g[(g.height-1, x)]
#     for point, elem in g.ray_from_with_index((g.height-1, x), Direction.NORTH):
#         if elem > m:
#             visible.add(point)
#             m = elem

# for y in range(g.height):
#     visible.add((y, 0))
#     m = g[(y, 0)]
#     for point, elem in g.ray_from_with_index((y, 0), Direction.EAST):
#         if elem > m:
#             visible.add(point)
#             m = elem
#     visible.add((y, g.width-1))
#     m = g[(y, g.width-1)]
#     for point, elem in g.ray_from_with_index((y, g.width-1), Direction.WEST):
#         if elem > m:
#             visible.add(point)
#             m = elem
# print(len(visible))

view = []
for point, cur in g.row_major_with_index():
    score = 1
    for dir in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
        see = 0
        for seen in g.ray_from(point, dir):
            see += 1
            if seen >= cur:
                score *= see
                break
        else:
            score *= see
                
    view.append((score, point))

print(max(view))
