from itertools import pairwise, permutations
from aoc_utils import *
from aocd import get_data

import re

data = get_data(year=2015, day=9, block=True)


def parse_graph(data):
    graph = {}
    locations = set()

    for line in data.splitlines():
        m = re.match(r"(.*) to (.*) = (\d+)", line)
        start, end, cost = m.groups()
        graph[(start, end)] = int(cost)
        graph[(end, start)] = int(cost)
        locations.add(start)
        locations.add(end)

    return graph, locations


def part_one(data):
    graph, locations = parse_graph(data)

    mc = None
    for route in permutations(locations):
        cost = 0
        for a, b in pairwise(route):
            cost += graph[(a, b)]

        if mc is None or cost < mc:
            mc = cost

    return mc


def part_two(data):
    graph, locations = parse_graph(data)

    mc = None
    for route in permutations(locations):
        cost = 0
        for a, b in pairwise(route):
            cost += graph[(a, b)]

        if mc is None or cost > mc:
            mc = cost

    return mc


print(part_one(data))
print(part_two(data))
