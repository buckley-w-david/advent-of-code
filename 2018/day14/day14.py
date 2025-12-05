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

from aoc_utils import *

def part_one(start):
    data = [3, 7]
    start = int(start)
    elves = [0, 1]

    for _ in range(start + 10):
        ev1 = data[elves[0]]
        ev2 = data[elves[1]]

        mixed_score = ev1 + ev2

        if mixed_score >= 10:
            data.append(mixed_score // 10)
            data.append(mixed_score % 10)
        else:
            data.append(mixed_score)

        elves[0] = (elves[0] + ev1+1) % len(data)
        elves[1] = (elves[1] + ev2+1) % len(data)

    return ''.join(map(str, data[start:start+10]))

def part_two(target):
    data = [3, 7]
    elves = [0, 1]

    target = [int(c) for c in target]
    pattern_size = len(target)

    i = 2
    while data[-pattern_size:] != target and data[-pattern_size-1:-1] != target:
        ev1 = data[elves[0]]
        ev2 = data[elves[1]]

        mixed_score = ev1 + ev2

        if mixed_score >= 10:
            data.append(mixed_score // 10)
            data.append(mixed_score % 10)
            i += 1
        else:
            data.append(mixed_score)

        elves[0] = (elves[0] + ev1+1) % len(data)
        elves[1] = (elves[1] + ev2+1) % len(data)

        i += 1

    if data[-pattern_size-1:-1] == target:
        i -= 1

    return i-pattern_size

print(part_one("681901"))
print(part_two("681901"))
