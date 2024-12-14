from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=13, block=True)

A_COST = 3
B_COST = 1


def cost(a, b):
    return A_COST * a + B_COST * b


# My part one implementation looks terrible when compared to part two
def part_one(data):
    machines = data.split("\n\n")
    tokens = 0
    for machine in machines:
        lines = machine.splitlines()
        (ax, ay) = ints(lines[0])
        (bx, by) = ints(lines[1])
        target = tuple(ints(lines[2]))

        def neighbour(node):
            (x, y), (step_a, step_b) = node
            next = []
            if step_a <= 100:
                next.append((A_COST, ((x + ax, y + ay), (step_a + 1, step_b))))
            if step_b <= 100:
                next.append((B_COST, ((x + bx, y + by), (step_a, step_b + 1))))
            return next

        graph = LazyGraph(neighbour)
        dijkstra = graph.dijkstra(((0, 0), (0, 0)))
        winners = [(p, q) for (p, q) in dijkstra.predecessors.keys() if p == target]
        if not winners:
            continue
        best = min(winners, key=lambda pq: cost(*pq[1]))
        tokens += cost(*best[1])
    return tokens


def part_two(data):
    machines = data.split("\n\n")
    tokens = 0
    for machine in machines:
        lines = machine.splitlines()
        a1, a2 = ints(lines[0])
        b1, b2 = ints(lines[1])
        c1, c2 = ints(lines[2])
        c1 += 10000000000000
        c2 += 10000000000000

        det = a1 * b2 - a2 * b1
        if det == 0:
            continue

        # Had to break out a pen and paper to remember how to do intersection of lines
        x = (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1)
        y = (c1 * a2 - c2 * a1) / (b1 * a2 - a1 * b2)
        if not x.is_integer() or not y.is_integer():
            continue

        tokens += int(x * A_COST + y * B_COST)

    return tokens


print(part_one(data))
print(part_two(data))
