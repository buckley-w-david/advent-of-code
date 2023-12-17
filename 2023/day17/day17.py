from aoc_utils import * # type: ignore
from aocd import get_data
import heapq

from typing import NamedTuple

class Direction(NamedTuple):
    dx: int
    dy: int

EAST = Direction(1, 0)
WEST = Direction(-1, 0)
NORTH = Direction(0, -1)
SOUTH = Direction(0, 1)

data = get_data(year=2023, day=17, block=True)
grid = Grid([[int(c) for c in l] for l in data.splitlines()])

# d = direction
# s = streak
#        y  x  d     s
start = (0, 0, EAST, 0)
target = (grid.height-1, grid.width-1)

def edges_with_weight(p):
    y, x, direction, streak = p
    dx, dy = direction
    prev_y, prev_x = y-dy, x-dx

    transitions = []

    if (y, x) == target:
        return

    if p == start:
        transitions.append((1, 0, SOUTH, 1))
        transitions.append((0, 1, EAST, 1))

    if streak >= 4:
        if direction == NORTH or direction == SOUTH:
            transitions.append((y, x+1, EAST, 1))
            transitions.append((y, x-1, WEST, 1))
        else:
            transitions.append((y+1, x, SOUTH, 1))
            transitions.append((y-1, x, NORTH, 1))

    if 1 <= streak < 10:
        transitions.append((y+dy, x+dx, direction, streak+1))

    for point in transitions:
        (py, px, _, next_streak) = point
        if (py, px) == target and next_streak < 4:
            continue
        if (py, px) == (prev_y, prev_x):
            continue
        if (py, px) not in grid:
            continue

        cost = grid[py, px]
        yield (cost, point)


inf = float('inf')
dist = { start: 0 }
prev = { }
pq = [(0, start)]
history = set()

while pq:
    _, u = heapq.heappop(pq)
    if u in history:
        continue
    history.add(u)
    for cost, v in edges_with_weight(u):
        if v in history:
            continue

        alt = dist[u] + cost
        if alt < dist.get(v, inf):
            dist[v] = alt
            prev[v] = u
            heapq.heappush(pq, (alt, v))

from functools import cache

class DijkstraResult:
    def __init__(self, start, distances, predecessors):
        self.start = start
        self.distances = distances
        self.predecessors = predecessors

    def distance_to(self, target) -> int:
        return self.distances[target]

    @cache
    def path_to(self, target):
        path = []
        node = target
        while node is not self.start:
            path.append(node)
            node = self.predecessors[node]
        path.append(node)
        path.reverse()
        return path

d = DijkstraResult(start, dist, prev)
md = float('inf')
for (y, x, h, v), distance in dist.items():
    if (y, x) == target:
        if distance <= md:
            md = distance
            point = (y, x, h, v)

print(md)
