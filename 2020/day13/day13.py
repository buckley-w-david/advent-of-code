#!/usr/bin/env python

from aocd import get_data, submit
from aoc_utils import Grid, Direction
import math

data = get_data(year=2020, day=13, block=True)
# data = """
# 939
# 7,13,x,x,59,x,31,19
# """.strip()

lines = data.splitlines()
arrival = int(lines[0])
ids = [int(i) for i in lines[1].split(",") if i != "x"]

a = []
for id in ids:
    div = arrival / id
    a.append((id, abs(math.ceil(div)-div)))

(bus_id, d) = min(a, key=lambda b: b[1])
div = arrival / bus_id
factor = abs(math.ceil(div))
diff = bus_id*factor-arrival
rint(bus_id*diff)
