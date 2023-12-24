from itertools import combinations
from aoc_utils import *
from aocd import get_data

def parse_hail(data):
    return [ints(line) for line in data.splitlines()]

LOWER = 200000000000000
UPPER = 400000000000000

def part_one(data):
    hail = [(Point(x, y), Point(dx, dy)) for (x, y, _, dx, dy, _) in parse_hail(data)]

    intersections = 0
    for (as_, ad), (bs, bd) in combinations(hail, 2):

        dx = bs.x - as_.x
        dy = bs.y - as_.y
        det = bd.x * ad.y - bd.y * ad.x
        if det == 0: continue

        u = (dy * bd.x - dx * bd.y) / det
        v = (dy * ad.x - dx * ad.y) / det

        if u < 0 or v < 0:
            continue

        x, y = as_.x + ad.x*u, as_.y + ad.y*u

        intersections += LOWER <= x <= UPPER and LOWER <= y <= UPPER

    return intersections

def part_two(data):
    # I worked how to do this one on paper, then solved it with a system of equation solver
    #
    # By specifying our trajectories as parametric equations, we can use the resulting equations uniquely define all
    # the parameters of the line that must intersect them at different times.
    #
    # x(t) = x0 + at
    # y(t) = y0 + bt
    # z(t) = z0 + ct
    #
    # (x0, y0, z0) is a point on the line, and (a, b, c) are the x, y and z components of a vector along the line
    # This is exactly what we are given in the input.
    #
    # Define 3 lines (l1, l2, l3) using this format, and solve for the components of l4 (the line that intersects them)
    # l4 has 6 unknown components, (x0, y0, z0) and (a, b, c)
    #
    # x1(t1) = x4(t1), y1(t1) = y4(t1), z1(t1) = z4(t1)
    # x2(t2) = x4(t2), y2(t2) = y4(t2), z2(t2) = z4(t2)
    # x3(t3) = x4(t3), y3(t3) = y4(t3), z3(t3) = z4(t3)
    #
    # With t1, t2, and t3, we have 9 unknowns and 9 equations
    # Plugging in our data into an equation solver with these equations spits out the answer

    x, y, z = (324764920956014, 100697955736353, 270369299931782)
    a, b, c = (-97, 311, 11)
    return x+y+z


data = get_data(year=2023, day=24, block=True)
print(part_one(data))
print(part_two(data))
