#!/usr/bin/env python

from aocd import get_data, submit

import re

data = get_data(year=2020, day=14, block=True)
# data = """
# mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# mem[8] = 11
# mem[7] = 101
# mem[8] = 0
# """.strip()


# data = """
# mask = 000000000000000000000000000000X1001X
# mem[42] = 100
# mask = 00000000000000000000000000000000X0XX
# mem[26] = 1
# """.strip()

pattern = re.compile(r"mem\[(\d+)\]")

memory = {}
mask = 0
masks_float = []

from more_itertools import powerset

for line in data.splitlines():
    op, val = line.split(" = ")
    if op == "mask":
        masks_float = []
        mask_or = int(val.replace('X', '0'), 2)
        float_idx = {idx for idx, v in enumerate(reversed(val)) if v == 'X'}
        bit_length = len(val)
        for ones in powerset(float_idx):
            zeros = float_idx - set(ones)
            float_and_mask = (1 << bit_length+1) - 1
            float_or_mask = 0
            for zero in zeros:
                float_and_mask ^= (1 << zero)
            for one in ones:
                float_or_mask ^= (1 << one)
            masks_float.append((float_and_mask, float_or_mask))
    else:
        val = int(val)
        idx = int(pattern.match(op).group(1)) | mask_or
        for idx_and_mask, idx_or_mask in masks_float:
            memory[(idx | idx_or_mask) & idx_and_mask] = val

print(sum(memory.values()))
