
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

from typing import Union
def resolve(target) -> Union[float, int]:
    v = monkeys[target]
    if isinstance(v, tuple):
        l, op, r = v
        return eval(f"({resolve(l)}){op}({resolve(r)})")
    return v
    
# Just by manual checking humn ends up in the left hand side
l, _, r = monkeys["root"]
target = resolve(r)

lower = 0
upper = 10000000000000 # Manually determined this as an upper bound
def guess(n: int) -> Union[float, int]:
    monkeys["humn"] = n
    # Negate the result because there is an inverse relationship between guess and result
    # larger guess means smaller value.
    # This screws with the binary search implementation
    # We can get around that by negating both target and result
    return -resolve(l)

idx = binary_search(lower, upper, guess, -target)
print(idx)
