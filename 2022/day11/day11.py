#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

import re

data = get_data(year=2022, day=11, block=True)

lines = data.splitlines()

monkeys = {}
factor = 1
for i in range(0, len(lines), 7):
    g = lines[i:i+7]
    n = ints(g[0])[0]
    items = ints(g[1])
    op = re.search(r"Operation: new = (.*)", g[2]).group(1)
    test = int(re.search(r"Test: divisible by (.*)", g[3]).group(1))
    t = int(re.search(r"If true: throw to monkey (.*)", g[4]).group(1))
    f = int(re.search(r"If false: throw to monkey (.*)", g[5]).group(1))

    factor *= test

    monkeys[n] = {
        "n": n,
        "items": items,
        "op": op,
        "test": test,
        "t": t,
        "f": f,
        "count": 0,
    }

for round in range(10000):
    for n in monkeys:
        monkey = monkeys[n]
        while monkey["items"]:
            worry = monkey["items"][0]
            monkey["items"] = monkey["items"][1:]
            monkey["count"] += 1
            test = monkey["test"]
            t = monkey["t"]
            f = monkey["f"]
            old = worry

            new = eval(monkey["op"])
            # new = math.floor(new / 3)
            if new % test == 0:
                target = t
            else:
                target = f
            monkeys[target]["items"].append(new % factor)

print([(m["n"], m["count"]) for m in sorted(monkeys.values(), key=lambda m: m["count"], reverse=True)])
