#!/usr/bin/env python

from collections import defaultdict
from aocd import get_data, submit
import re

print("\033[2J\033[H") # ]]

data = get_data(year=2020, day=24, block=True)
# data = """
# sesenwnenenewseeswwswswwnenewsewsw
# neeenesenwnwwswnenewnwwsewnenwseswesw
# seswneswswsenwwnwse
# nwnwneseeswswnenewneswwnewseswneseene
# swweswneswnenwsewnwneneseenw
# eesenwseswswnenwswnwnwsewwnwsene
# sewnenenenesenwsewnenwwwse
# wenwwweseeeweswwwnwwe
# wsweesenenewnwwnwsenewsenwwsesesenwne
# neeswseenwwswnwswswnw
# nenwswwsewswnenenewsenwsenwnesesenew
# enewnwewneswsewnwswenweswnenwsenwsw
# sweneswneswneneenwnewenewwneswswnese
# swwesenesewenwneswnwwneseswwne
# enesenwswwswneneswsenwnewswseenwsese
# wnwnesenesenenwwnenwsewesewsesesew
# nenewswnwewswnenesenwnesewesw
# eneswnwswnwsenenwnwnwwseeswneewsenese
# neswnwewnwnwseenwseesewsenwsweewe
# wseweeenwnesenwwwswnew
# """.strip()

dp = {
    "e": (1, 0),
    "se": (0.5, 1),
    "sw": (-0.5, 1),
    "w": (-1, 0),
    "nw": (-0.5, -1),
    "ne": (0.5, -1),
}

def around(p):
    x, y = p
    for _, vector in dp.items():
        dx, dy = vector
        yield x+dx, y+dy

reference = (0, 0)
lines = data.splitlines()

instruction = re.compile('e|se|sw|w|nw|ne')
is_black_tile = defaultdict(bool)

for line in lines:
    steps = instruction.findall(line)
    x, y = reference
    for step in steps:
        dx, dy = dp[step]
        x += dx
        y += dy
    is_black_tile[x, y] = not is_black_tile[x, y]

active = { tile for tile, state in is_black_tile.items() if state }

from more_itertools import flatten
for _ in range(100):
    next_gen = set()
    points_of_interest = flatten(map(around, active))
    for p in points_of_interest:
        p_active = p in active
        c = len(active.intersection(around(p)))
        if p_active and (1 <= c <= 2):
            next_gen.add(p)
        elif not p_active and c == 2:
            next_gen.add(p)
    active = next_gen
    print(len(active))

print(len(active))
