#!/usr/bin/env python

from itertools import combinations
from aocd import get_data, submit

data = get_data(year=2020, day=9, block=True)
# data = """
# 35
# 20
# 15
# 25
# 47
# 40
# 62
# 55
# 65
# 95
# 102
# 117
# 150
# 182
# 127
# 219
# 299
# 277
# 309
# 576
# """.strip()

numbers = [int(i) for i in data.split("\n")]

def first_invalid(numbers, memory):
    for i in range(memory, len(numbers)):
        n = numbers[i]
        corpus = numbers[i-memory:i]
        for (a, b) in combinations(corpus, 2):
            if a + b == n:
                break
        else:
            return n

invalid = first_invalid(numbers, 25)

for i in range(0, len(numbers)):
    for window_size in range(0, len(numbers)-i):
        r = numbers[i:i+window_size]
        if sum(r) == invalid:
            print(max(r) + min(r))
            exit()
