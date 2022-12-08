#!/usr/bin/env python

from aocd import get_data, submit
from aoc_utils import Grid, Direction
import math

data = get_data(year=2020, day=13, block=True)
# data = """
# 939
# 7,13,x,x,59,x,31,19
# """.strip()

# data = """
# 939
# 17,x,13,19
# """.strip()

lines = data.splitlines()

# Really ugly chinese remainder theorem implementation
# T + offset ~= busid -> T ~= -offset mod busid
# Theory leared from https://www.youtube.com/watch?v=zIFehsBHB8o
ids = [(int(i), -idx % int(i)) for idx, i in enumerate(lines[1].split(",")) if i != 'x' ]

ni, bi = list(zip(*ids))

N = 1
for n in ni:
    N *= n

modular_inverse = lambda x, mod: pow(x, -1, mod)

Ni = [N // n for n in ni]
xi = [modular_inverse(n, i) for n, i in zip(Ni, ni)]

p = [a*b*c for ((a,b),c) in zip(zip(bi, Ni), xi)]
print(sum(p) % N)
