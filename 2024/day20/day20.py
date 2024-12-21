from collections import deque
from itertools import combinations

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=20, block=True)


def parse(data):
    # In retrospect, this was the wrong way to go about solving the problem
    # It is also not easily generalizable to arbitrary length cheats
    grid = Grid.parse(data)
    start, end = None, None
    for yx, c in grid.row_major_with_index():
        if c == "S":
            start = yx
        elif c == "E":
            end = yx

    assert start
    assert end

    grid[start] = "."
    grid[end] = "."

    graph = Graph()

    history = set()
    queue = deque([(start, 2)])
    while queue:
        node = queue.popleft()
        if node in history:
            continue
        history.add(node)

        yx, cheat = node
        for ayx, c in grid.around_with_index(yx, corners=False):
            if c == ".":
                nn = (ayx, max(cheat - 1, 0) if cheat != 2 else cheat)
                graph.add_edge(node, nn)
                queue.append(nn)
            elif c == "#" and cheat > 1:
                nn = (ayx, cheat - 1)
                graph.add_edge(node, nn)
                queue.append(nn)
    return graph, start, end, grid


def part_one(data):
    graph, start, end, _ = parse(data)
    d1 = graph.dijkstra((start, 2))
    cheatless = d1.distance_to((end, 2))
    d2 = graph.dijkstra((end, 2))

    candidates = set()
    t = 0
    for (yx, c), d in d2.distances.items():
        if c == 1:
            d_start = d1.distance_to((yx, 1))
            if cheatless - (d_start + d) >= 100:
                t += 1
                candidates.add((yx, d))

    return t


def cheat_destinations(yx, stride=20):
    sy, sx = yx
    for y in range(-stride - 1, stride + 1):
        for x in range(-stride + abs(y), stride - abs(y) + 1):
            yield (sy + y, sx + x), abs(x) + abs(y)


def part_two(data):
    # dijkstra (and even the graph representation itself) is _super_ overkill for this
    # but since I already have the method...
    graph, start, end, _ = parse(data)
    dij = graph.dijkstra((start, 2))
    cheatless_distance = dij.distance_to((end, 2))
    path = [yx for yx, _ in dij.path_to((end, 2))]

    distances = {yx: i for i, yx in enumerate(path)}
    t = 0
    for cheat_start in path:
        for cheat_end, d in cheat_destinations(cheat_start):
            if (
                cheat_end not in distances
                or distances[cheat_start] > distances[cheat_end]
            ):
                continue
            total = distances[cheat_start] + d + (distances[end] - distances[cheat_end])
            diff = cheatless_distance - total
            if diff >= 100:
                t += 1
    return t


print(part_one(data))
print(part_two(data))
