#!/usr/bin/env python

import math
from itertools import permutations
from pprint import pprint
from aocd import get_data, submit
import re

print("\033[2J\033[H") # ]]


data = get_data(year=2020, day=20, block=True)
#data = """
#Tile 2311:
#..##.#..#.
###..#.....
##...##..#.
#####.#...#
###.##.###.
###...#.###
#.#.#.#..##
#..#....#..
####...#.#.
#..###..###

#Tile 1951:
##.##...##.
##.####...#
#.....#..##
##...######
#.##.#....#
#.###.#####
####.##.##.
#.###....#.
#..#.#..#.#
##...##.#..

#Tile 1171:
#####...##.
##..##.#..#
###.#..#.#.
#.###.####.
#..###.####
#.##....##.
#.#...####.
##.##.####.
#####..#...
#.....##...

#Tile 1427:
####.##.#..
#.#..#.##..
#.#.##.#..#
##.#.#.##.#
#....#...##
#...##..##.
#...#.#####
#.#.####.#.
#..#..###.#
#..##.#..#.

#Tile 1489:
###.#.#....
#..##...#..
#.##..##...
#..#...#...
######...#.
##..#.#.#.#
#...#.#.#..
###.#...##.
#..##.##.##
####.##.#..

#Tile 2473:
##....####.
##..#.##...
##.##..#...
#######.#.#
#.#...#.#.#
#.#########
#.###.#..#.
#########.#
###...##.#.
#..###.#.#.

#Tile 2971:
#..#.#....#
##...###...
##.#.###...
###.##..#..
#.#####..##
#.#..####.#
##..#.#..#.
#..####.###
#..#.#.###.
#...#.#.#.#

#Tile 2729:
#...#.#.#.#
#####.#....
#..#.#.....
#....#..#.#
#.##..##.#.
#.#.####...
#####.#.#..
###.####...
###..#.##..
##.##...##.

#Tile 3079:
##.#.#####.
#.#..######
#..#.......
#######....
#####.#..#.
#.#...#.##.
##.#####.##
#..#.###...
#..#.......
#..#.###...
#""".strip()
 

from tile import Tile

from collections import Counter

tiles = set()
for tile in data.split('\n\n'):
    tiles.add(Tile.parse(tile.strip()))

corners = set()
for t1 in tiles:
    edges = list(t1.edges())
    matching_edges = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
    }
    for t2 in tiles:
        if t1 is t2:
            continue
        oe = list(t2.edges())
        for id1, e1 in edges:
            for id2, e2 in oe:
                if e1 == e2:
                    matching_edges[id1 % 4] += 1

    # Every edge maps to exactly one other edge (2 because of flips)
    assert max(matching_edges.values()) == 2
    c = Counter(matching_edges.values())
    if c[0] >= 2:
        corners.add((t1, tuple([id for (id, c) in matching_edges.items() if c == 0])))




def assemble_picture(tiles, corners):
    remaining = tiles - {t for t, _ in corners}
    c0, c1, c2, c3 = corners

    a = [c0, (c0[0], c0[1][::-1])]
    b = [c1, (c1[0], c1[1][::-1])]
    c = [c2, (c2[0], c2[1][::-1])]
    d = [c3, (c3[0], c3[1][::-1])]
    s = int(math.sqrt(len(tiles)))
    counter = 0
    for c0 in a:
        for c1 in b:
            for c2 in c:
                for c3 in d:
                    for tl, tr, br, bl in permutations([c0, c1, c2, c3]):
                        print(counter)
                        counter += 1

                        # Step one
                        # Map edges into their corner orientation through flips/rotations
                        # tl -> (3, 0)
                        # tl -> (0, 1)
                        # br -> (1, 2)
                        # bl -> (2, 3)
                        top_left_tile = tl[0]
                        for transform in Tile.find_adjacent_edge_transformation(tl[1], (3, 0)):
                            top_left_tile = transform(top_left_tile)
                        top_right_tile = tr[0]
                        for transform in Tile.find_adjacent_edge_transformation(tr[1], (0, 1)):
                            top_right_tile = transform(top_right_tile)
                        bottom_right_tile = br[0]
                        for transform in Tile.find_adjacent_edge_transformation(br[1], (1, 2)):
                            bottom_right_tile = transform(bottom_right_tile)
                        bottom_left_tile = bl[0]
                        for transform in Tile.find_adjacent_edge_transformation(bl[1], (2, 3)):
                            bottom_left_tile = transform(bottom_left_tile)

                        grid = [[None for _ in range(s)] for _ in range(s)]
                        grid[0][0] = top_left_tile
                        grid[0][s-1] = top_right_tile
                        grid[s-1][s-1] = bottom_right_tile
                        grid[s-1][0] = bottom_left_tile

                        remaining_tiles = remaining.copy()
                        def place_tile(grid, tile):
                            for orientation in tile.permutations():
                                for y in range(s):
                                    for x in range(s):
                                        if grid[y][x] is None:
                                            t = False
                                            m = True
                                            if x != 0 and grid[y][x-1] is not None:
                                                m &= (orientation.edge(3) == grid[y][x-1].edge(1))
                                                t = True
                                            if x != s-1 and grid[y][x+1] is not None:
                                                m &= (orientation.edge(1) == grid[y][x+1].edge(3))
                                                t = True
                                            if y != 0 and grid[y-1][x] is not None:
                                                m &= (orientation.edge(0) == grid[y-1][x].edge(2))
                                                t = True
                                            if y != s-1 and grid[y+1][x] is not None:
                                                m &= (orientation.edge(2) == grid[y+1][x].edge(0))
                                                t = True
                                            if m and t:
                                                return (y, x), orientation

                        while remaining_tiles:
                            progress = False
                            for tile in remaining_tiles:
                                placement = place_tile(grid, tile)
                                if placement is not None:
                                    (y, x), orientation = placement
                                    grid[y][x] = orientation
                                    progress = True
                                    remaining_tiles.remove(tile)
                                    break
                            if not progress:
                                # print(tl[1], tr[1], br[1], bl[1], "made no progress")
                                # This orientation of corners is incorrect
                                break
                        else:
                            assert all(grid[y][x] is not None for x in range(s) for y in range(s))
                            return grid

picture = assemble_picture(tiles, corners)
# fp = []
# s = int(math.sqrt(len(tiles)))
# for y in range(10*s):
#     row = []
#     for x in range(10*s):
#         idx_y = y // 10
#         idx_x = x // 10

#         ty = y % 10
#         tx = x % 10
#         tile = picture[idx_y][idx_x]
#         row.append((ty, tx) in tile.points)
#     fp.append(row)


# mega_tile = Tile.from_grid(0, fp)
# print(mega_tile.rotated().rotated().rotated())

# Strip borders
def strip_borders(tile):
    fp = []
    for y in range(1, 9):
        row = []
        for x in range(1, 10):
            row.append((y, x) in tile.points)
        fp.append(row)
    return Tile.from_grid(tile.id, fp)
s = int(math.sqrt(len(tiles)))
picture_without_borders = [[None for _ in range(len(picture))] for _ in range(len(picture))]
for y, row in enumerate(picture):
    for x, tile in enumerate(row):
        picture_without_borders[y][x] = strip_borders(tile)

fp = []
for y in range(8*s):
    row = []
    for x in range(8*s):
        idx_y = y // 8
        idx_x = x // 8

        ty = y % 8
        tx = x % 8
        tile = picture_without_borders[idx_y][idx_x]
        row.append((ty, tx) in tile.points)
    fp.append(row)

mega_tile = Tile.from_grid(0, fp)
print(mega_tile.rotated().rotated().rotated())

import pickle
# This takes a while to run, save it to a file so I can write the rest of the logic with the results later
with open('mega_tile.pickle', 'wb') as f:
    pickle.dump(mega_tile, f)
print('JOBS DONE')
