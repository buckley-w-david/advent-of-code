from collections import defaultdict, deque

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=10, block=True)


def part_one(data):
    grid = Grid.parse(data, cast=int)
    graph = Graph()
    head_candidates = set()
    tail_candidates = set()

    for yx, h1 in grid.row_major_with_index():
        if h1 == 0:
            head_candidates.add(yx)
        elif h1 == 9:
            tail_candidates.add(yx)

        for ayx, h2 in grid.around_with_index(yx, corners=False):
            if h2 == h1 + 1:
                graph.add_edge(yx, ayx)

    score = 0
    for head in head_candidates:
        dijkstra = graph.dijkstra(head)
        for tail in tail_candidates:
            points = dijkstra.path_to(tail)
            if points:
                score += 1

    return score


def part_two(data):
    grid = Grid.parse(data, cast=int)
    graph = Graph()
    head_candidates = set()
    tail_ratings = defaultdict(int)

    for yx, h1 in grid.row_major_with_index():
        if h1 == 0:
            head_candidates.add(yx)

        for ayx, h2 in grid.around_with_index(yx, corners=False):
            if h2 == h1 + 1:
                graph.add_edge(yx, ayx)

    for head in head_candidates:
        queue = deque([head])
        while queue:
            node = queue.pop()
            if grid[node] == 9:
                tail_ratings[node] += 1

            for other_node in graph.edges(node):
                queue.appendleft(other_node)

    return sum(tail_ratings.values())


print(part_one(data))
print(part_two(data))
