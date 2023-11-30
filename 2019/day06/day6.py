#!/usr/bin/env python

from aocd import get_data
from aoc_utils import *

data = get_data(year=2019, day=6)
lines = data.splitlines()

orbit_pairs = [line.split(")") for line in lines]
graph = Graph()
for i, o in orbit_pairs:
    graph.add_edge(i, o)
    graph.add_edge(o, i)

print(len(graph.dijkstra("YOU").path_to("SAN"))-3)
