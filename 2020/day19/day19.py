#!/usr/bin/env python

from collections import deque
from aocd import get_data, submit

import re

print("\033[2J\033[H") # ]]

data = get_data(year=2020, day=19, block=True)


static_rule = re.compile(r"^(\d+): \"([a-z]+)\"$")
reference_rule = re.compile(r"^(\d+): (.*)$")

rule_spec, messages = data.split("\n\n")
rules = {}

for line in rule_spec.splitlines():
    m = static_rule.match(line)
    if m:
        rules[m.group(1)] = m.group(2)
    else:
        m = reference_rule.match(line)
        idx = m.group(1)
        s = [tuple(n for n in s.strip().split()) for s in m.group(2).split("|")] 
        rules[idx] = s

max_message = max(len(l) for l in messages.splitlines())

# This is so dumb 
def build_rule(rule):
    if rule == '8':
        return f'(({build_rule("42")})+)'
    elif rule == '11':
        fourty_two = '(' + build_rule("42") + ')'
        thirty_one = '(' + build_rule("31") + ')'
        r = []
        for i in range(1, max_message//2 + 1):
            r.append(f"({fourty_two*i}{thirty_one*i})")
        # print(r)
        return '|'.join(r)

    rule = rules[rule]
    if isinstance(rule, str):
        return rule

    return '|'.join(''.join('('+build_rule(reference)+')' for reference in and_rule) for and_rule in rule)

rz = build_rule('0')
print(rz)
rule_zero = re.compile('^' + rz + '$')
# s = 0
# for line in messages.splitlines():
#     s += rule_zero.match(line) is not None
# print(s)
