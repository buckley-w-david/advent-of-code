from typing import cast
from collections import defaultdict, deque
from aoc_utils import *
from aocd import get_data

data = get_data(year=2023, day=25, block=True)

def parse_graph(data):
    graph = defaultdict(set)

    for line in data.splitlines():
        k, vs = line.split(": ")
        for v in vs.split():
            graph[k].add(v)
            graph[v].add(k)

    return graph


def part_one(data):
    graph = parse_graph(data)

    # partition graph via BFS
    # Found a very brief description of the technique here https://patterns.eecs.berkeley.edu/?page_id=571#1_BFS
    for start in graph:
        history = set(start)
        queue = cast(deque, deque([(start, 0)]))
        levels = {}
        while queue:
            node, level = queue.pop()

            levels[node] = level

            for other_node in graph[node]:
                if other_node in history: continue
                history.add(other_node)

                queue.appendleft((other_node, level+1))

        for level in range(min(levels.values()), max(levels.values())+1):
            p1 = set()
            p2 = set()
            for node in graph:
                if levels[node] <= level:
                    p1.add(node)
                else:
                    p2.add(node)

            connections = 0
            for node in p1:
                for conn in graph[node]:
                    connections += conn in p2

            if connections == 3:
                return len(p1)*len(p2)

print(part_one(data))
