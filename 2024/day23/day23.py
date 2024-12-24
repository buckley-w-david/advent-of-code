from collections import defaultdict
from itertools import combinations

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=23, block=True)


def parse(data):
    network = defaultdict(set)

    for line in data.splitlines():
        a, b = line.split("-")
        network[a].add(b)
        network[b].add(a)

    return network


def part_one(data):
    network = parse(data)
    candidates = [c for c in network if c[0] == "t"]
    t = 0
    history = set()
    for candidate in candidates:
        for a, b in combinations(network[candidate], 2):
            if b in network[a] and a in network[b]:
                subgraph = frozenset([candidate, a, b])
                t += subgraph not in history
                history.add(subgraph)
    return t


def part_two(data):
    network = parse(data)
    computers = set(network.keys())

    # Bron-Kerbosch algorithm
    # Finds all maximal cliques
    def _find(partial, candidates, exclude):
        if not candidates and not exclude:
            yield partial
        else:
            for candidate in list(candidates):
                if candidate in exclude:
                    continue
                yield from _find(
                    partial.union([candidate]),
                    candidates.intersection(network[candidate]),
                    exclude.intersection(network[candidate]),
                )
                candidates.remove(candidate)
                exclude.add(candidate)

    max_clique = max(_find(set(), set(computers), set()), key=lambda c: len(c))
    return ",".join(sorted(max_clique))


print(part_one(data))
print(part_two(data))
