from collections import defaultdict
import re
from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=16, block=True)
analysis = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}
sues = defaultdict(dict)
for line in data.splitlines():
    sue, stats = re.split(r": ", line, 1)
    attributes = re.findall(r"([^ ]+): (\d+)", line)
    for name, quantity in attributes:
        sues[sue][name] = int(quantity)

invalid = set()
for sue, stats in sues.items():
    for attribute, constraint in analysis.items():
        if attribute == "cats" or attribute == "trees":
            if attribute in stats and stats[attribute] <= constraint:
                invalid.add(sue)
                break
        elif attribute == "pomeranians" or attribute == "goldfish":
            if attribute in stats and stats[attribute] >= constraint:
                invalid.add(sue)
                break
        else:
            if attribute in stats and stats[attribute] != constraint:
                invalid.add(sue)
                break

for sue in sues.keys():
    if sue not in invalid:
        print(sue)
        break
