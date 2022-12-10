#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data


data = get_data(year=2022, day=10, block=True)
lines = iter(data.splitlines())

t = 0

X = 1
i = 1

waiting = 0

px = 0

try: 
    while True:
        dx, dy = px%40, px // 40
        px += 1
        if dx == X or dx == X-1 or dx == X+1:
            print('#', end='')
        else:
            print('.', end='')
        if px % 40 == 0:
            print()

        if waiting:
            X += waiting
            waiting = 0
        else:
            line = next(lines)
            if line.startswith("noop"):
                pass
            else:
                _, waiting = line.split()
                waiting = int(waiting)
        i += 1

        if (i + 20) % 40 == 0:
            t += X * i
except StopIteration:
    pass
    # print(t) - Part 1
