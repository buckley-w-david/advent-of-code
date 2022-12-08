#!/usr/bin/env python

from collections import defaultdict
from aocd import get_data, submit
import re

print("\033[2J\033[H") # ]]

data = get_data(year=2020, day=25, block=True)
# data = """
# 5764801
# 17807724
# """.strip()

cpk, dpk = map(int, data.splitlines())

def transform(subject_number, loop_size):
    v = 1
    for _ in range(loop_size):
        v *= subject_number
        v %= 20201227
    return v


pk = 1
cls = 0
while pk != cpk:
    cls += 1
    pk *= 7
    pk %= 20201227

# pk = -1
# dls = 0
# while pk != dpk:
#     dls += 1
#     pk = transform(7, dls)
# print(dls)

print(transform(dpk, cls))
