from collections import defaultdict
from itertools import pairwise

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=14, block=True)


WIDTH = 101
HEIGHT = 103


def advance(p, v, seconds=100):
    px, py = p
    dx, dy = v

    return ((px + dx * seconds) % WIDTH, (py + dy * seconds) % HEIGHT)


def score(robots):
    q1, q2, q3, q4 = 0, 0, 0, 0
    hx = int(WIDTH / 2)
    hy = int(HEIGHT / 2)
    for x, y in robots:
        if x < hx:
            if y < hy:
                q1 += 1
            elif y > hy:
                q2 += 1
        elif x > hx:
            if y < hy:
                q3 += 1
            elif y > hy:
                q4 += 1
    return q1 * q2 * q3 * q4


def part_one(data):
    robots = []
    for line in data.splitlines():
        px, py, vx, vy = ints(line)
        x, y = advance((px, py), (vx, vy), 100)
        robots.append((x, y))

    return score(robots)


def display(robots):
    rb = {p for p, _ in robots}
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) in rb:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def suspicious(robots, tolerance=10):
    rb = defaultdict(set)
    for (x, y), _ in robots:
        rb[y].add(x)

    for _, xs in rb.items():
        consecutive = 0
        for a, b in pairwise(sorted(xs)):
            consecutive += a + 1 == b
            if consecutive > tolerance:
                return True
    return False


def part_two(data):
    robots = set()
    for line in data.splitlines():
        px, py, vx, vy = ints(line)
        p = (px, py)
        v = (vx, vy)
        robots.add((p, v))

    gen = 0
    while True:
        next_gen = set()
        for p, v in robots:
            q = advance(p, v, 1)
            next_gen.add((q, v))
        robots = next_gen
        gen += 1

        if suspicious(robots):
            display(robots)
            # Not sure I've written an interactive advent of code solution before...
            if input("Enter 'y' if there is a tree: ") == "y":
                return gen


print(part_one(data))
print(part_two(data))
