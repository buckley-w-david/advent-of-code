#!/usr/bin/env python

from aocd import get_data, submit
from collections import Counter
from functools import cache

data = get_data(year=2020, day=10, block=True)
# data = """
# 28
# 33
# 18
# 42
# 31
# 14
# 46
# 20
# 48
# 47
# 24
# 23
# 49
# 45
# 19
# 38
# 39
# 11
# 1
# 32
# 25
# 35
# 8
# 17
# 7
# 9
# 4
# 2
# 34
# 10
# 3
# """.strip()

numbers = [int(i) for i in data.split("\n")]
tree = {
    i: tuple(range(i+1, i+4))
    for i in numbers
}

tree[0] = (1, 2, 3)
m = max(numbers)+3


@cache
def count_leaves(element):
    leaves = 0
    for connection in tree[element]:
        if connection in tree:
            leaves += count_leaves(connection)
        elif connection == m:
            leaves += 1
    return leaves

print(count_leaves(0))
