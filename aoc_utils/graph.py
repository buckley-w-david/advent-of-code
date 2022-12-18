import abc
from collections import defaultdict
try:
    from functools import cache
except ImportError:
    from functools import lru_cache
    cache = lru_cache(None)
import heapq
from typing import TypeVar, Generic, Iterable, Callable, Tuple, Set, Iterator

T = TypeVar("T")

class Dijkstra:
    def __init__(self, start, distances, predecessors):
        self.start = start
        self.distances = distances
        self.predecessors = predecessors

    def distance_to(self, target: T) -> int:
        return self.distances[target]

    @cache
    def path_to(self, target: T) -> list[T]:
        path = []
        node = target
        while node is not self.start:
            path.append(node)
            node = self.predecessors[node]
        path.append(node)
        path.reverse()
        return path


class NodeGraph(Generic[T], abc.ABC):
    @abc.abstractmethod
    def edges(self, node: T) -> Iterable[T]:
        ...

    def dijkstra(self, start: T) -> Dijkstra:
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
            for cost, v in self.edges(u):
                if v in history:
                    continue

                alt = dist[u] + cost
                if alt < dist.get(v, inf):
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(pq, (alt, v))
        return Dijkstra(start, dist, prev)

class Graph(NodeGraph[T]):
    def __init__(self):
        self._edges = defaultdict(set)
        super().__init__()

    def add_edge(self, p: T, q: T, weight=1):
        self._edges[p].add((weight, q))

    def edges(self, node: T) -> Set[T]:
        return self._edges[node]


class LazyGraph(NodeGraph[T]):
    def __init__(self, neighbour_fn: Callable[[T], Iterable[Tuple[int, T]]]):
        self.neighbour_fn = neighbour_fn

    def edges(self, node: T) -> Iterator[Tuple[int, T]]:
        yield from self.neighbour_fn(node)
