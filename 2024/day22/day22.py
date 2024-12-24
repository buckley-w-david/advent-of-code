from collections import defaultdict
import re
from itertools import pairwise

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=22, block=True)


def mix(a, b):
    return a ^ b


assert mix(42, 15) == 37


def prune(seed):
    return seed % 16_777_216


assert prune(100000000) == 16113920


def rand(seed):
    r = seed * 64
    seed = prune(mix(seed, r))
    r = seed // 32
    seed = prune(mix(seed, r))
    r = seed * 2048
    seed = prune(mix(seed, r))
    return seed


seed = 123
seed = rand(seed)
assert seed == 15887950
seed = rand(seed)
assert seed == 16495136
seed = rand(seed)
assert seed == 527345
seed = rand(seed)
assert seed == 704524
seed = rand(seed)
assert seed == 1553684
seed = rand(seed)
assert seed == 12683156
seed = rand(seed)
assert seed == 11100544
seed = rand(seed)
assert seed == 12249484
seed = rand(seed)
assert seed == 7753432
seed = rand(seed)
assert seed == 5908254


def part_one(data):
    seeds = list(map(int, data.splitlines()))
    for _ in range(2000):
        seeds = [rand(seed) for seed in seeds]
    return sum(seeds)


def part_two(data):
    prices = []
    seeds = list(map(int, data.splitlines()))
    for _ in range(2000):
        prices.append([seed % 10 for seed in seeds])
        seeds = [rand(seed) for seed in seeds]
    changes = {i: [] for i in range(len(seeds))}
    for a, b in pairwise(prices):
        for i, (ai, bi) in enumerate(zip(a, b)):
            changes[i].append(bi - ai)

    sums = defaultdict(int)
    for monkey, diffs in changes.items():
        history = set()
        for i in range(4, len(diffs)):
            sequence = diffs[i - 4: i]
            seq = tuple(sequence)
            if seq in history:
                continue
            history.add(seq)
            sums[seq] += prices[i][monkey]
    return max(sums.values())


print(part_one(data))
print(part_two(data))
