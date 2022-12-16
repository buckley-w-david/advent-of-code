#!/usr/bin/env python

from collections import deque, namedtuple
from dataclasses import dataclass
from typing import List
import re

from aocd import get_data

data = get_data(year=2022, day=16, block=True)
d = {}

Valve = namedtuple('Valve', ['rate', 'leads_to'])

to_sel = {}
by_name = {}
initial_state = 0
for i, line in enumerate(sorted(data.splitlines())):
    name, rate, to = re.match(r"Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line).groups()
    r = int(rate)
    by_name[name] = (r, to.split(", "))

    sel = 1 << i
    to_sel[name] = sel
    initial_state |= (r == 0) << i

def sel(name):
    return to_sel[name]

valves = {}
for name, (rate, to) in by_name.items():
    valves[to_sel[name]] = Valve(rate, list(map(sel, to)))

max_state = 2 ** len(valves) - 1
max_pressure = 0
best = {}

queue = deque()
queue.appendleft((sel("AA"), sel("AA"), initial_state, 26, 0))

while queue:
    msel, esel, state, remaining, pressure = queue.pop()
    if (msel, esel, state) in best and pressure <= best[(msel, esel, state)]:
        continue

    best[(msel, esel, state)] = pressure

    if (remaining <= 0 or state == max_state) and pressure > max_pressure:
        max_pressure = pressure
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

print(max_pressure)
