#!/usr/bin/env python

from collections import deque
from aocd import get_data, submit

print("\033[2J\033[H") # ]]

data = get_data(year=2020, day=23, block=True)
# data = """
# 389125467
# """.strip()

labels = [int(n) for n in data]
midx = max(labels)
circle = {a: b for a, b in zip(labels, labels[1:])}
for a, b in zip(range(midx+1, 1000001), range(midx+2, 1000001)):
    circle[a] = b
circle[labels[-1]] = midx+1
circle[1000000] = labels[0]
current = labels[0]

midx = 1000000

def take(n, start):
    a = start
    for _ in range(n):
        a = circle[a]
        yield a

for i in range(10000000):
    selected = list(take(3, current))
    a, b, c = selected
    circle[current] = circle[c]

    dest = current-1
    if dest == 0:
        dest = midx
    while dest in selected:
        dest -= 1
        if dest == 0:
            dest = midx

    circle[c] = circle[dest]
    circle[dest] = a

    current = circle[current]

print(circle[1]*circle[circle[1]])
