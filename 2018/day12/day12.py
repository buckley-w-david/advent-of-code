from aocd import get_data
from aoc_utils import *

data = get_data(year=2018, day=12, block=True)

def part_one(data):
    state, rule_spec = data.split("\n\n")
    pots = { i for i, c in enumerate(state.split()[2]) if c == '#' }
    rules = {}
    for line in rule_spec.splitlines():
        pattern, result = line.split(" => ")
        rules[tuple(c == '#' for c in pattern)] = result == '#'

    # FIXME: this does many duplicate checks
    for _ in range(20):
        next_pots = set()
        for pot in pots:
            # because the empty pattern ..... maps to .
            # we only have to check near currently active pots
            for candidate in range(pot-4, pot+5):
                pattern = tuple(i in pots for i in range(candidate-2, candidate+3))
                if rules[pattern]:
                    next_pots.add(candidate)
        pots = next_pots

    return sum(pots)

def serialize(pots):
    return ''.join('#' if i in pots else '.' for i in range(min(pots), max(pots)+1))

def part_two(data):
    state, rule_spec = data.split("\n\n")
    pots = { i for i, c in enumerate(state.split()[2]) if c == '#' }
    rules = {}
    for line in rule_spec.splitlines():
        pattern, result = line.split(" => ")
        rules[tuple(c == '#' for c in pattern)] = result == '#'

    next_pots = set()
    for i in range(50_000_000_000):
        next_pots = set()
        for pot in pots:
            for candidate in range(pot-4, pot+5):
                pattern = tuple(i in pots for i in range(candidate-2, candidate+3))
                if rules[pattern]:
                    next_pots.add(candidate)

        # Janky way to detect when we've reached a steady state
        # I noticed by visual inspection that after enough generations
        # we reach a point where the pattern of plants stops changing
        # and instead everything just starts increasing by one every generation
        if serialize(pots) == serialize(next_pots):
            diff = sum(next_pots) - sum(pots)
            return sum(pots) + (50_000_000_000-i)*diff

        pots = next_pots

    # We should never reach here
    return sum(pots)

print(part_one(data))
print(part_two(data))
