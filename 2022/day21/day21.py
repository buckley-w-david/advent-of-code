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
    if isinstance(v, int):
        return v
    else:
        l, op, r = v
        return eval(f"({resolve(l)}){op}({resolve(r)})")
    
# Just by manual checking humn ends up in the left hand side
l, _, r = monkeys["root"]
target = resolve(r)

lower = 0
upper = 10000000000000 # Manually determined this as an upper bound
while lower != upper:
    guess = (lower + upper) // 2
    monkeys["humn"] = guess
    result = resolve(l)
    if result == target:
        break
    elif target > result:
        # This is the reverse of the normal adjustment in a binary search
        # Typically we'd adjust the lower bound upwards here
        # However there is an inverse relationship between guess and the result
        # Decreasing the guess increases the result
        upper = guess - 1
    else:
        lower = guess + 1
print(lower)
