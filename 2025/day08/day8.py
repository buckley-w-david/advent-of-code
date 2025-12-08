from functools import reduce
import itertools
import math
from operator import mul
from aocd import get_data

from aoc_utils.union_find import UnionFind
from aoc_utils import maxn

data = get_data(year=2025, day=8, block=True)


def parse(data):
    return [tuple(int(n) for n in line.split(",")) for line in data.splitlines()]


def part_one(data):
    points = parse(data)
    circuits = UnionFind(points)
    d = []
    # FIXME: How can I avoid calculating all combinations?
    for a, b in itertools.combinations(points, 2):
        d.append((math.dist(a, b), a, b))
    d.sort()

    for i in range(1000):
        _, a, b = d[i]
        circuits.union(a, b)

    return reduce(mul, maxn(circuits.size.values(), 3))


def part_two(data):
    points = parse(data)
    circuits = UnionFind(points)
    d = []
    # FIXME: How can I avoid calculating all combinations?
    for a, b in itertools.combinations(points, 2):
        d.append((math.dist(a, b), a, b))
    d.sort()

    reference = points[0]
    i = 0
    a, b = None, None
    while circuits.size[circuits.find(reference)] != len(points):
        _, a, b = d[i]
        circuits.union(a, b)
        i += 1

    assert a
    assert b
    return a[0] * b[0]


print(part_one(data))
print(part_two(data))
