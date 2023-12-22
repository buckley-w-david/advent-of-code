from collections import defaultdict
import re

from aoc_utils import *
from aocd import get_data

def parse_snapshot(data):
    bricks = []
    for line in data.splitlines():
        s, e = line.split("~")
        (x, y, z), (xx, yy, zz) = sorted([ints(s), ints(e)], key=lambda t: tuple(reversed(t)))

        brick = [(_x, _y, _z) for _x in range(x, xx+1) for _y in range(y, yy+1) for _z in range(z, zz+1)]
        bricks.append(brick)

    return sorted(bricks, key=lambda b: b[0][2])

def intersections(stack, brick):
    return { stack[cube] for cube in brick if cube in stack }
            
def simulate(bricks):
    settled = set()

    depends_on = defaultdict(set)
    supports = defaultdict(set)

    stack = {}

    for i, brick in enumerate(bricks):
        collisions = []

        while brick[0][2] > 1:
            next_brick = [ (x, y, z-1) for (x, y, z) in brick ]
            collisions = intersections(stack, next_brick)
            if collisions:
                supports[i]
                for ob in collisions:
                    depends_on[i].add(ob)
                    supports[ob].add(i)

                break
            brick = next_brick
        else:
            supports[i]
            depends_on[i]

        for point in brick:
            stack[point] = i

    return depends_on, supports

def part_one(data):
    falling_bricks = parse_snapshot(data)

    depends_on, supports = simulate(falling_bricks)

    redundant = 0
    for brick, supporting in supports.items():
        for supported in supporting:
            if len(depends_on[supported]) == 1:
                break
        else:
            redundant += 1

    return redundant

import copy

def part_two(data):
    falling_bricks = parse_snapshot(data)

    depends_on, supports = simulate(falling_bricks)

    fallout = [0]*len(falling_bricks)

    for brick, supporting in supports.items():
        if not supporting: continue

        # What can I say? I got lazy
        depends_copy, supports_copy = copy.deepcopy(depends_on), copy.deepcopy(supports)

        queue = set()
        for supported in supporting:
            if len(depends_on[supported]) == 1:
                queue.add(supported)
        del supports_copy[brick]

        i = 0
        while queue:
            to_remove = queue.pop()
            for supported in supports_copy[to_remove]:
                depends_copy[supported].remove(to_remove)
                if not depends_copy[supported]:
                    queue.add(supported)

            del supports_copy[to_remove]

            i += 1
        fallout[brick] = i

    return sum(fallout)


data = get_data(year=2023, day=22, block=True)

print(part_one(data))
print(part_two(data))
