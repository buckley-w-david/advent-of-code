from collections import deque, defaultdict
import heapq

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=16, block=True)


def parse(data):
    grid = Grid.parse(data)
    graph = Graph()

    start, target = None, None
    for yx, c in grid.row_major_with_index():
        if c == "S":
            start = yx
        elif c == "E":
            target = yx

    assert start
    assert target

    grid[start] = "."
    grid[target] = "."

    queue = deque([(start, Direction.EAST)])
    history = set()

    while queue:
        n = queue.popleft()
        if n in history:
            continue
        history.add(n)

        yx, d = n
        rt = d.rotate(handedness=+1, cardinal=True)
        lt = d.rotate(handedness=-1, cardinal=True)

        if grid[yx + rt] == ".":
            graph.add_edge((yx, d.value), (yx, rt.value), weight=1000)
            queue.append((yx, rt))

        if grid[yx + lt] == ".":
            graph.add_edge((yx, d.value), (yx, lt.value), weight=1000)
            queue.append((yx, lt))

        if grid[yxr := yx + d] == ".":
            graph.add_edge((yx, d.value), (yxr, d.value), weight=1)
            queue.append((yxr, d))

    return start, target, graph


def part_one(data):
    start, target, graph = parse(data)
    dij = graph.dijkstra((start, Direction.EAST.value))

    # Since we include direction as part of graph nodes, we need to check arriving at the target node from each direction
    return min(dij.distance_to((target, d.value)) for d in Direction.cardinal())


# Dijkstra with multiple predecessors
def dijkstra(graph, start):
    inf = float("inf")
    dist = {start: 0}
    prev = defaultdict(set)
    pq = [(0, start)]
    history = set()

    while pq:
        _, u = heapq.heappop(pq)
        if u in history:
            continue
        history.add(u)
        for cost, v in graph.edges_with_weight(u):
            if v in history:
                continue

            alt = dist[u] + cost
            if alt < dist.get(v, inf):
                dist[v] = alt
                prev[v] = {u}
                heapq.heappush(pq, (alt, v))
            elif alt == dist.get(v, inf):
                dist[v] = alt
                prev[v].add(u)
                heapq.heappush(pq, (alt, v))

    return dist, prev


def part_two(data):
    start, target, graph = parse(data)

    dist, prev = dijkstra(graph, (start, Direction.EAST.value))
    md = min(
        (d for d in Direction.cardinal() if (target, d.value) in dist),
        key=lambda d: dist[(target, d.value)],
    )

    queue = deque([(target, md.value)])
    points = set()
    while queue:
        node = queue.popleft()
        yx, _ = node
        points.add(yx)

        for n in prev[node]:
            queue.append(n)

    return len(points)


print(part_one(data))
print(part_two(data))
