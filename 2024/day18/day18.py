from collections import deque

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=18, block=True)
GRID_SIZE = 71


def part_one(data):
    grid = Grid([["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)])
    for i, line in enumerate(data.splitlines()):
        if i == 1024:
            break
        x, y = ints(line)
        grid[y, x] = "#"

    graph = Graph()
    queue = deque([(0, 0)])
    history = set()
    while queue:
        yx = queue.popleft()
        if yx in history:
            continue
        history.add(yx)
        for nyx, c in grid.around_with_index(yx, corners=False):
            if c != "#":
                queue.append(nyx)
                graph.add_edge(yx, nyx)
                graph.add_edge(nyx, yx)

    dij = graph.dijkstra((0, 0))
    return dij.distance_to((GRID_SIZE - 1, GRID_SIZE - 1))


def part_two(data):
    grid = Grid([["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)])
    graph = Graph()
    queue = deque([(0, 0)])
    history = set()
    while queue:
        yx = queue.popleft()
        if yx in history:
            continue
        history.add(yx)
        for nyx, _ in grid.around_with_index(yx, corners=False):
            queue.append(nyx)
            graph.add_edge(yx, nyx)
            graph.add_edge(nyx, yx)

    best_path = None
    for line in data.splitlines():
        x, y = ints(line)
        grid[y, x] = "#"
        yx = (y, x)
        del graph._edges[yx]
        for ayx, _ in grid.around_with_index(yx, corners=False):
            graph._edges[ayx].discard(yx)

        if best_path is None or yx in best_path:
            dij = graph.dijkstra((0, 0))
            path = dij.path_to((GRID_SIZE - 1, GRID_SIZE - 1))
            if path is None:
                return yx
            best_path = set(path)


print(part_one(data))
print(part_two(data))
