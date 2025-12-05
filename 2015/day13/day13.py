from itertools import permutations, pairwise
from collections import defaultdict
import re

from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=13, block=True)


def parse(data):
    rules = defaultdict(dict)

    for line in data.splitlines():
        m = re.match(
            r"(.*) would (gain|lose) (\d+) happiness units by sitting next to (.*).",
            line,
        )

        target, sign, amount, source = m.groups()
        rules[target][source] = int(amount) * (-1 if sign == "lose" else 1)

    return rules


def optimal_arrangement(rules):
    # There simply aren't that many people in the input, we can brute force it
    max_change = None
    optimal = None
    for seating in permutations(rules.keys()):
        change = 0
        for a, b in pairwise(seating):
            change += rules[a][b]
            change += rules[b][a]
        change += rules[seating[0]][seating[-1]]
        change += rules[seating[-1]][seating[0]]

        if max_change is None or max_change < change:
            optimal = seating
            max_change = change

    return optimal, max_change


def part_one(data):
    rules = parse(data)
    return optimal_arrangement(rules)[1]


def part_two(data):
    rules = parse(data)
    for target in list(rules.keys()):
        rules[target]["me"] = 0
        rules["me"][target] = 0

    return optimal_arrangement(rules)[1]


def part_two_alt(data):
    rules = parse(data)
    arrangement, best_change = optimal_arrangement(rules)
    worst_change = None
    for a, b in pairwise(arrangement):
        change = rules[a][b] + rules[b][a]
        if worst_change is None or worst_change > change:
            worst_change = change

    # arrangement warps around, so we have to account for the first + last pair as well
    change = (
        rules[arrangement[0]][arrangement[-1]] + rules[arrangement[-1]][arrangement[0]]
    )
    return best_change - min(worst_change, change)


print(part_one(data))
print(part_two(data))
print(part_two_alt(data))
