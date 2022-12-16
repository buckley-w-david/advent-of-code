#!/usr/bin/env python

import re
from aocd import get_data

data = get_data(year=2022, day=16, block=True)

d = {}

from dataclasses import dataclass
from typing import List

@dataclass
class Valve:
    name: str
    rate: int
    leads_to: List[str]
    closed: bool = True
    idx: int = 0

    def selector(self):
        return 1 << self.idx

for line in data.splitlines():
    m = re.match(r"Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line)
    name, rate, valves = m.groups()
    d[name] = Valve(name, int(rate), valves.split(", "), int(rate) != 0)

max_state = 0
state = 0
translation = {}
valves = {}
for i, name in enumerate(sorted(d.keys())):
    d[name].idx = i
    if not d[name].closed:
        state |= (1 << i)
    max_state = (max_state << 1) | 1
    translation[name] = i


def sel(name):
    return d[name].selector()

for key, value in d.items():
    value.leads_to = list(map(sel, value.leads_to))
    valves[value.selector()] = value

from collections import deque
queue = deque()

queue.appendleft((sel("AA"), sel("AA"), state, 26, 0))

s = 0
best = {}

while queue:
    node = queue.pop()
    msel, esel, state, remaining, pressure = node
    # print(msel, esel, bin(state), remaining)
    if (msel, esel, state) in best and pressure <= best[(msel, esel, state)]:
        continue

    best[(msel, esel, state)] = pressure

    if (remaining <= 0 or state == max_state) and pressure > s:
        s = pressure
        continue

    mt = None
    if (msel & state) == 0:
        state |= (max_state & msel)
        pressure += valves[msel].rate * (remaining-1)
        mt = msel

    et = None
    if (esel & state) == 0:
        state |= (max_state & esel)
        pressure += valves[esel].rate * (remaining-1)
        et = esel

    if mt and et:
        queue.appendleft((mt, et, state, remaining - 1, pressure))
    elif mt:
        for v in valves[esel].leads_to:
            queue.appendleft((mt, v, state, remaining - 1, pressure))
    elif et:
        for v in valves[msel].leads_to:
            queue.appendleft((v, et, state, remaining - 1, pressure))
    else:
        for mv in valves[msel].leads_to:
            for ev in valves[esel].leads_to:
                queue.appendleft((mv, ev, state, remaining - 1, pressure))

print(s)
