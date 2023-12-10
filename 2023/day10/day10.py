# Grid, Direction
# Direction.NORTH,SOUTH,EAST,WEST,NE,SE,NW,SW
# g = Grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# g.width, g.height, (y, x) in g (coords), g[(y, x)], g[(y, x)] = 5
# for item in g => iterate over items in row major order
# g.row_major(_with_index)() => iterate over items in row major order
# g.column_major(_with_index)() => iterate over items in column major order
# g.apply(func) => call func with each item
# g.map(func) => return new Grid with results of func
# g.ray_from((y, x), direction), yields items from a starting point in a direction
# g.around(_with_index) => What it sounds like

# Graph
# g = Graph()
# g.add_edge(from, to, weight=something)
# g.dijkstra(start) => Dijkstra (has `distance_to`, and `path_to` methods)

# ShuntingYard
# Expression parser with configurable precedence for operations so you can throw out (B)EDMAS (no support for brackets)

from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=10, block=True)
lines = data.splitlines()
horizontal = ['-']*len(lines[0])
vertical = ['|']*len(lines[0])
higher_res = []
for line in lines:
    l = zip(line, horizontal)
    hl = zip(vertical, horizontal)
    higher_res.append(''.join(''.join(t) for t in l))
    higher_res.append(''.join(''.join(t) for t in hl))
g = Grid([[c for c in line] for line in higher_res])
pipes = {}
start = None

def write_c(s, colour=False):
    if colour:
        print(end=f'\N{ESC}[31m{s}\u001b[0m') # ]]
        pass
    else:
        print(end=s)

def display_pipes(network):
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
                write_c(c, colour=(not y&1 and not x&1))
            else:
                write_c(' ', colour=(not y&1 and not x&1))
        print()

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

covered = {None}
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

    connect_to_start = set()
    for p in network:
        p1, p2 = pipes[p]
        if p1 == start or p2 == start:
            connect_to_start.add(p)

    if len(connect_to_start) == 2:
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
            display_pipes(network)
            assert start in pipes[p]

            network.add(start)
            print(len(network) / 2)

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
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        cy = p[0] + dy
                        cx = p[1] + dx
                        if 0 <= cy < g.height and 0 <= cx < g.width and (cy, cx) != p:
                            queue.add((cy, cx))
            surrounded = 0
            for (y, x), _ in g.row_major_with_index():
                if not y&1 and not x&1:
                    # This is an original tile
                    if (y, x) not in network and (y, x) not in outside:
                        surrounded += 1
            print(surrounded)
            break



        del pipes[start]

# 831 too high
