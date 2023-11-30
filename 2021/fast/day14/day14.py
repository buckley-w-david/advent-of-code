#!/usr/bin/env python

from aocd import get_data

data = get_data(year=2021, day=14, block=True)

template, rules = data.split("\n\n")
rules = [rule.split(" -> ") for rule in rules.splitlines()]
rules = {a: b for a, b in rules}

from collections import Counter, defaultdict

pairs = [''.join(pair) for pair in zip(template, template[1:])]

all_chars = defaultdict(int)
for char in template:
    all_chars[char] += 1

template = Counter(pairs)
for _ in range(40):
    c = defaultdict(int)
    for pair in template:
        a, b = pair
        between = rules[pair]
        count = template[pair]
        all_chars[between] += count
        c[a+between] += count
        c[between+b] += count
    template = c

s = max(all_chars.values())-min(all_chars.values())
print(s)
