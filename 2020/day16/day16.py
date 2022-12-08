#!/usr/bin/env python

from collections import defaultdict
from aocd import get_data, submit
import re
import numpy as np

print("\033[2J\033[H") # ]]

data = get_data(year=2020, day=16, block=True)
# data = """
# class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19

# your ticket:
# 11,12,13

# nearby tickets:
# 3,9,18
# 15,1,5
# 5,14,9
# """.strip()

p = re.compile(r"([\w ]+): (.*)") 
rules_lines, my_ticket, other_tickets = data.split("\n\n")
other_tickets = [list(map(int, ticket.split(","))) for ticket in other_tickets.splitlines()[1:]]

my_ticket = [int(n) for n in my_ticket.splitlines()[1].split(",")]

rules = { }
for line in rules_lines.strip().splitlines():
    m = p.match(line)
    name = m.group(1)
    ranges = m.group(2)
    valid = set()
    for spec in ranges.split(" or "):
        l, u = spec.split("-")
        valid |= set(range(int(l), int(u)+1))
    rules[name] = valid

alpha_rules = np.array(sorted(rules.keys()))
labels_idx = {
    name: None for name in rules
}

valid_tickets = []
for ticket in other_tickets:
    valid = all([any([n in rule for rule in rules.values()]) for n in ticket])
    if not valid:
        continue
    valid_tickets.append(ticket)

# while None in labels_idx.values():
print(alpha_rules)
s = len(rules)

while None in labels_idx.values():
    matches = []
    for ticket in valid_tickets:
        match = [[False]*len(ticket)]*len(ticket)
        match = np.zeros((s, s), dtype=np.int8)
        for i, n in enumerate(ticket):
            for ri, rule in enumerate(alpha_rules):
                match[i][ri] = n in rules[rule]
        matches.append(match)
    matches = np.array(matches)
    for i, v in enumerate(alpha_rules):
        if labels_idx[v] is not None:
            matches[:, :, i] = 0
    for i in range(s):
        idx = np.product(matches[:, i, :], axis=0)
        if idx.sum() == 1:
            labels_idx[alpha_rules[idx == 1][0]] = i
print(labels_idx)
print(my_ticket)
p = 1
for label, idx in labels_idx.items():
    if label.startswith("departure"):
        p *= my_ticket[idx]
print(p)
