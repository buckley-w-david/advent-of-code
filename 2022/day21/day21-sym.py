#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

data = get_data(year=2022, day=21, block=True)
lines = data.splitlines()

monkeys = {}

import re

for line in lines:
    if (m := re.match(r"(.*): (-?\d+)", line)):
        monkey, n = m.groups()
        monkeys[monkey] = int(n)
    elif (m := re.match(r"(.*): (.*) (.) (.*)", line)):
        monkey, l, op, r = m.groups()
        monkeys[monkey] = (l, op, r)

def resolve(target):
    v = monkeys[target]
    if isinstance(v, tuple):
        l, op, r = v
        return eval(f"({resolve(l)}){op}({resolve(r)})")
    return v
    
from sympy import symbols
x = symbols('x')
monkeys["humn"] = x

l, _, r = monkeys["root"]

left = resolve(l)
right = resolve(r)

from sympy import solve
ans = solve(right - left, x)
print(int(ans[0]))
