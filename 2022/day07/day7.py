#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

from pathlib import Path
import re

data = get_data(year=2022, day=7, block=True)
lines = data.splitlines()
t = 0

filesystem =  { "/": {}}
path = Path("/") 

state = 0
for line in lines:
    m = re.match(r"\$ (.*)", line)
    if m:
        state = 0
        command = m.group(1)
        parts = command.split()
        if parts[0] == "cd":
            if parts[1] == "..":
                path = path.parent
            elif parts[1] == "/":
                path = Path("/")
            else:
                path = path / parts[1]
        elif parts[0] == "ls":
            state = 1
    elif state == 1:
        m = re.match(r"(\d+) (.*)", line)
        if m:
            size, name = m.groups()
            d = filesystem
            for p in path.parts:
                d = d[p]
            d[name] = int(size)
        m = re.match(r"dir (.*)", line)
        if m:
            name = m.group(1)
            d = filesystem
            for p in path.parts:
                d = d[p]
            d[name] = {}

sizes = []
def calc_size(d) -> int:
    t = 0
    for k, v in d.items():
        if isinstance(v, int):
            t += v
        else:
            t += calc_size(v)
    sizes.append(t) # gross
    return t

used = calc_size(filesystem["/"])
total = 70000000
target = 30000000

unused = total - used
diff = target - unused

print(min([s for s in sizes if s >= diff]))
