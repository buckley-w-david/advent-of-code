from collections import defaultdict
try:
    from functools import cache
except ImportError:
    from functools import lru_cache
    cache = lru_cache(None)
import heapq

class Dijkstra:
    def __init__(self, start, distances, predecessors):
        self.start = start
        self.distances = distances
        self.predecessors = predecessors

    def distance_to(self, target):
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


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)

    def add_edge(self, p, q, weight=1):
        self.nodes.add(p)
        self.nodes.add(q)
        self.edges[p].add((weight, q))

    def dijkstra(self, start):
        if start not in self.nodes:
            raise ValueError(f"{start} is not in the graph")

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
            for cost, v in self.edges[u]:
                if v in history:
                    continue

                alt = dist[u] + cost
                if alt < dist.get(v, inf):
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(pq, (alt, v))
        return Dijkstra(start, dist, prev)
