#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

data = get_data(year=2022, day=5, block=True)
crates, instructions = data.split("\n\n")

crates = crates.splitlines()[:-1]
instructions = instructions.splitlines()

buckets = { i: [] for i in range(1, 10) }

for line in crates:
    for idx, i in enumerate(range(1, len(line), 4)):
        crate = line[i]
        if crate == ' ':
            continue
        buckets[idx+1] = [crate] + buckets[idx+1]

import re
for ins in instructions:
    n, s, e = re.findall(r"\d+", ins)
    n, s, e = int(n), int(s), int(e)

    buckets[e].extend(buckets[s][-n:])
    buckets[s] = buckets[s][:-n]


for b in buckets.values():
    print(b[-1], end='')
