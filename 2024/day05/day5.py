from collections import defaultdict

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=5, block=True)


def parse(data):
    rules_blob, thing = data.split("\n\n")

    rules = defaultdict(set)

    for a, b in [ints(line) for line in rules_blob.splitlines()]:
        rules[a].add(b)

    updates = [ints(line) for line in thing.splitlines()]

    return rules, updates


def part_one(data):
    rules, updates = parse(data)
    mid = 0
    for update in updates:
        seen = set()
        all = set(update)
        for cp in update:
            if cp not in rules:
                seen.add(cp)
                continue

            if rules[cp] & all and rules[cp] & seen:
                break

            seen.add(cp)
        else:
            mid += update[int(len(update) / 2)]

    return mid


def part_two(data):
    rules, updates = parse(data)
    unordered = []

    for update in updates:
        seen = set()
        all = set(update)
        for cp in update:
            if cp not in rules:
                seen.add(cp)
                continue

            if rules[cp] & all and rules[cp] & seen:
                unordered.append(update)
                break

            seen.add(cp)

    mid = 0
    for update in unordered:
        final = []
        while update:
            all = set(update)
            for i, cp in enumerate(update):
                if not (rules[cp] & all):
                    final.append(update.pop(i))
                    break
        mid += final[int(len(final) / 2)]

    return mid


print(part_one(data))
print(part_two(data))
