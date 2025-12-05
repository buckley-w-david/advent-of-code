from functools import cache
from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=15, block=True)

ingredients = []
for line in data.splitlines():
    name, _ = line.split(":")
    ingredients.append(ints(line))


def score(recipe):
    capacity, durability, flavor, texture = 0, 0, 0, 0
    for i, quantity in enumerate(recipe):
        capacity += quantity * ingredients[i][0]
        durability += quantity * ingredients[i][1]
        flavor += quantity * ingredients[i][2]
        texture += quantity * ingredients[i][3]

    return max(capacity, 0) * max(durability, 0) * max(flavor, 0) * max(texture, 0)


def calories(recipe):
    return sum(quantity * ingredients[i][4] for i, quantity in enumerate(recipe))


@cache
def find_max(recipe, remaining):
    if remaining == 0:
        return score(recipe)

    ms = 0
    for i in range(len(ingredients)):
        nr = (*recipe[:i], recipe[i] + 1, *recipe[i + 1:])

        s = find_max(nr, remaining - 1)
        if s > ms:
            ms = s

    return ms


@cache
def find_max_constrained(recipe, remaining, target):
    if remaining == 0:
        if calories(recipe) != target:
            return 0
        return score(recipe)

    ms = 0
    for i in range(len(ingredients)):
        nr = (*recipe[:i], recipe[i] + 1, *recipe[i + 1:])
        if calories(nr) > target:
            continue

        s = find_max_constrained(nr, remaining - 1, target)
        if s > ms:
            ms = s

    return ms


def part_one(data):
    initial = tuple(0 for _ in range(len(ingredients)))
    return find_max(initial, 100)


def part_two(data):
    initial = tuple(0 for _ in range(len(ingredients)))
    return find_max_constrained(initial, 100, 500)


print(part_one(data))
print(part_two(data))
