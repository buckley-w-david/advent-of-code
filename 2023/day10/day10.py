from collections import Counter, deque
from pprint import pprint
from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=10, block=True)
lines = data.splitlines()

def alternating(*iterables):
    for values in zip(*iterables):
        for value in values:
            yield value

# By interspersing - between every character horizontall and | vertically
# we double the resolution of the "map" without changing the connectivity of the
# looping network.
#
# The advantage of this increase resolution is that the small gaps between pipes become full tiles
# which makes part 2 much easier. A normal flood fill can be used to determine inside/outside.
#
# This does require a bit of care in the calculation to not count newly introduced tiles, and an adjustment for part 1
# but overall this seems like a much simpler solution than others that come to mind
horizontal = ['-']*len(lines[0])
vertical = ['|']*len(lines[0])*2
higher_res = []
for line in lines:
    higher_res.append(''.join(alternating(line, horizontal)))
    higher_res.append(vertical)

g = Grid([[c for c in line] for line in higher_res])

def display_network(network):
    for y in range(g.height):
        for x in range(g.width):
            p = (y, x)

            if p in network:
                c = g[p]
                match c:
                    case '|': c = "│"
                    case '-': c = "─"
                    case 'L': c = "└"
                    case 'J': c = "┘"
                    case '7': c = "┐"
                    case 'F': c = "┌"
                print(c, end='')
            else:
                print(end=' ')
        print()

def find_pipes():
    pipes = {}
    start = None
    for ((y, x), c) in g.row_major_with_index():
        dst = ( None, None )
        match c:
            case '|': dst = ((y+1, x), (y-1, x))
            case '-': dst = ((y, x+1), (y, x-1))
            case 'L': dst = ((y-1, x), (y, x+1))
            case 'J': dst = ((y-1, x), (y, x-1))
            case '7': dst = ((y, x-1), (y+1, x))
            case 'F': dst = ((y, x+1), (y+1, x))
            case 'S':
                start = (y, x)
                continue
            case _:
                continue
        pipes[(y, x)] = dst
    return start, pipes

def find_networks(pipes):
    covered = set()
    for p in pipes:
        if p in covered:
            continue

        covered.add(p)
        p1, p2 = pipes[p]
        queue = [(p, p1), (p, p2)]
        network = {p}
        while queue:
            src, dst = queue.pop()
            if dst not in pipes or src not in pipes[dst]:
                continue

            network.add(dst)
            covered.add(dst)

            p1, p2 = pipes[dst]

            if p1 not in covered:
                queue.append((dst, p1))
            if p2 not in covered:
                queue.append((dst, p2))

        yield network

def part_one():
    start, pipes = find_pipes()
    for network in find_networks(pipes):
        connect_to_start = set()
        for p in network:
            p1, p2 = pipes[p]
            if p1 == start or p2 == start:
                connect_to_start.add(p)

        if len(connect_to_start) != 2:
            continue

        pipes[start] = tuple(connect_to_start)

        visited = set()
        p = start
        while len(visited) != len(network):
            visited.add(p)
            p1, p2 = pipes[p]
            if p1 not in visited:
                p = p1
            elif p2 not in visited:
                p = p2
            elif len(visited) != len(network):
                # We've reached a dead-end
                break
        else:
            assert start in pipes[p]

            network.add(start)
            # extra // 2 because we've blown up the resolution 2 times to make part 2 easier
            return len(network) // 2 // 2

        del pipes[start]

def part_two():
    start, pipes = find_pipes()
    for network in find_networks(pipes):
        connect_to_start = set()
        for p in network:
            p1, p2 = pipes[p]
            if p1 == start or p2 == start:
                connect_to_start.add(p)

        if len(connect_to_start) != 2:
            continue

        pipes[start] = tuple(connect_to_start)

        visited = set()
        p = start
        while len(visited) != len(network):
            visited.add(p)
            p1, p2 = pipes[p]
            if p1 and p1 not in visited:
                p = p1
            elif p2 and p2 not in visited:
                p = p2
            elif len(visited) != len(network):
                # We've reached a dead-end
                break
        else:
            assert start in pipes[p]
            network.add(start)

            # I know from visual inspection that (0, 0) is not enclosed by the loop
            outside = set()
            queue = set()
            queue.add((0, 0))
            while queue:
                p = queue.pop()
                if p in outside:
                    # Already visited this tile
                    continue
                elif p in network:
                    # Blocked by a pipe
                    continue
                outside.add(p)
                for pc, _ in g.around_with_index(p):
                    queue.add(pc)

            surrounded = 0
            for (y, x), _ in g.row_major_with_index():
                # Even x and y means tile is in the original un-expanded map
                if not (y&1 or x&1):
                    # This is an original tile
                    if (y, x) not in network and (y, x) not in outside:
                        surrounded += 1
            return surrounded

        del pipes[start]

print(part_one())
print(part_two())
