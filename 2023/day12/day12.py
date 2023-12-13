from functools import cache
from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=12, block=True)

@cache
def solve(springs: str, groups: tuple) -> int:
    if not groups:
        # This is a hacky way of finding out we did it wrong
        # If there are '#' left in the springs then we have over-provisioned
        return int(all(s != '#' for s in springs))
    elif len(springs) < sum(groups):
        return 0
    elif springs[0] == '.':
        return solve(springs[1:], groups)

    t = 0
    if springs[0] == "?":
        t += solve(springs[1:], groups)

    current, *remaining = groups
    potential = springs[:current]

    # if the group formed by the current contigious spring number is all ? or #
    # and there is enough room for the group to start at this location
    if all(s != '.' for s in potential) and (len(springs) > current and springs[current] != '#' or len(springs) == current):
        # count the group as starting here
        t += solve(springs[current+1:], tuple(remaining))

    return t

def part_one(data):
    t = 0
    for line in data.splitlines():
        springs, g = line.split()
        groups = tuple(int(n) for n in g.split(','))
        t += solve(springs, groups)

    return t

def part_two(data):
    t = 0
    for line in data.splitlines():
        springs, g = line.split()
        groups = tuple(int(n) for n in g.split(','))
        t += solve('?'.join([springs]*5), groups * 5)

    return t

print(part_one(data))
print(part_two(data))
