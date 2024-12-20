from collections import defaultdict, deque, Counter
from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=20, block=True)
data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


def parse(data, cheat_length=2):
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
    queue = deque([(start, cheat_length)])
    while queue:
        node = queue.popleft()
        if node in history:
            continue
        history.add(node)

        yx, cheat = node
        for ayx, c in grid.around_with_index(yx, corners=False):
            if c == ".":
                # This is a little sketchy, not sure if I should keep it
                if ayx == end and cheat != cheat_length:
                    cheat = 0
                nn = (ayx, max(cheat - 1, 0) if cheat != cheat_length else cheat)
                graph.add_edge(node, nn)
                # I am worried that the lack of a backward facing edge will bite me
                # But maybe it's fine
                # graph.add_edge(nn, node)
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
    for (yx, c), d in d2.distances.items():
        if c == 1:
            candidates.add((yx, d))

    t = 0
    for yx, d in candidates:
        d_start = d1.distance_to((yx, 1))
        if cheatless - (d_start + d) >= 100:
            t += 1

    return t


def part_two(data):
    graph, start, end, grid = parse(data, 20)
    d1 = graph.dijkstra((start, 20))
    cheatless = d1.distance_to((end, 20))
    d2 = graph.dijkstra((end, 20))

    candidates = set()
    for (yx, c), d in d2.distances.items():
        if c == 19:
            candidates.add((yx, d))

    # Need to keep track of all start/end points for cheats
    # > Because this cheat has the same start and end positions as the one above,
    # > it's the same cheat, even though the path taken during the cheat is different:

    # BFS from all candidates looking for valid start points?
    # early exit if d2.distances[candidate] + len(path) > cheatless - 100
    grid.print([a for a, _ in d1.path_to((end, 0))])
    print()
    grid.print([a for a, _ in candidates])
    breakpoint()
    return 0


print(part_one(data))

# print(part_two(data))
