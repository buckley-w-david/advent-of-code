from collections import defaultdict
from typing import cast
from aoc_utils import *
from aocd import get_data

# This is a little gross, but it was really easy to implement
def find_longest_path(graph, start):
    distances = defaultdict(int)
    visited = set()
    def search(node, current):
        nonlocal distances, visited

        if node in visited:
            return

        visited.add(node)

        if distances[node] < current:
            distances[node] = current

        for p, length in graph[node]:
            search(p, current+length)

        visited.remove(node)

    search(start, 0)

    return distances

def parse_graph(data, undirected=False):
    grid = Grid([[c for c in line] for line in data.splitlines()])

    start = (0, 1)
    end = (grid.height-1, grid.width-2)

    visited = set()
    graph = defaultdict(set)

    queue = cast(list, [(start, 1, (1, 1))])

    while queue:
        segment_start, segment_length, node = queue.pop()
        if node in visited: continue
        visited.add(node)

        if node == end:
            graph[segment_start].add((node, segment_length))
            # if undirected:
            #     graph[node].add((segment_start, segment_length))
        elif grid[node] != '.' and segment_start != node:
            # Branching points in the maze are marked by v and >
            # We use these points as endpoints in a graph
            # The regular path tiles between these endpoints are compacted into
            # a weight on the connection betweeen those endpoints
            graph[segment_start].add((node, segment_length))
            if undirected:
                graph[node].add((segment_start, segment_length))

            crossroad = None
            for p, c in grid.around_with_index(node, corners=False):
                if c == '.' and p not in visited:
                    crossroad =  p

            if crossroad is None:
                # If there is no unvisited crossroad then we have arrived at this point from another route
                # we can safely move on
                continue

            visited.add(crossroad)

            endpoints = [p for p, c in grid.around_with_index(crossroad, corners=False) if c != '#']

            for endpoint in endpoints:
                # Technically when undirected=False endpoint => crossroad isn't always true
                # It doesn't actually matter though in this problem because we can't get to the the invalid connections without
                # passing through the crossroad, making it invalid to visit it again anyway
                graph[endpoint].add((crossroad, 1))
                graph[crossroad].add((endpoint, 1))

                for p, c in grid.around_with_index(endpoint, corners=False):
                    if c == '.' and p not in visited:
                        if undirected or (endpoint[0] < p[0] and grid[endpoint] == 'v') or (endpoint[1] < p[1] and grid[endpoint] == '>'):
                            queue.append((endpoint, 0, endpoint))
        else:
            for p, c in grid.around_with_index(node, corners=False):
                if c == '#': continue

                queue.append((segment_start, segment_length+1, p))

    return start, end, graph

def part_one(data):
    start, end, graph = parse_graph(data)
    distances = find_longest_path(graph, start)
    return distances[end]

def part_two(data):
    start, end, graph = parse_graph(data, undirected=True)
    distances = find_longest_path(graph, start)
    return distances[end]

data = get_data(year=2023, day=23, block=True)

print(part_one(data))
print(part_two(data))
