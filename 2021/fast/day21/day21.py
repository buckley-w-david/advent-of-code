#!/usr/bin/env python

from aocd import get_data

data = get_data(year=2021, day=21, block=True)

import re
p1, p2 = data.splitlines()
p1_pos = int(re.search(r"starting position: (\d+)", p1).group(1))
p2_pos = int(re.search(r"starting position: (\d+)", p2).group(1))

sums = []
for a in range(1, 4):
    for b in range(1, 4):
        for c in range(1, 4):
            sums.append(a+b+c)
from collections import Counter
distributions = Counter(sums)

from functools import cache

@cache
def game(p1_pos, p2_pos, p1_score, p2_score, turn, die):
    if turn:
        p2_pos = ((p2_pos - 1 + die) % 10) + 1
        p2_score += p2_pos
    else:
        p1_pos = ((p1_pos - 1 + die) % 10) + 1
        p1_score += p1_pos

    if p1_score > 20:
        return ( 1, 0 )
    if p2_score > 20:
        return ( 0, 1 )

    turn = not turn

    w1 = 0
    w2 = 0
    for roll, count in distributions.items():
        r = game(p1_pos, p2_pos, p1_score, p2_score, turn, roll)
        w1 += count*r[0]
        w2 += count*r[1]
    return (w1, w2)


w1 = 0
w2 = 0
turn = 0
for roll, count in distributions.items():
    r = game(p1_pos, p2_pos, 0, 0, 0, roll) 
    w1 += count*r[0]
    w2 += count*r[1]

print(max(w1, w2))
