from collections import deque
from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=12, block=True)


def parse(data):
    grid = Grid.parse(data)
    regions = []
    history = set()
    for yx, c in grid.row_major_with_index():
        if yx in history:
            continue
        queue = deque([yx])
        region = set([yx])
        while queue:
            np = queue.popleft()
            for ayx, cc in grid.around_with_index(np, corners=False):
                if cc != c or ayx in history:
                    continue
                history.add(ayx)

                region.add(ayx)
                queue.append(ayx)
        regions.append(region)
    return regions


def around(point):
    y, x = point

    yield (y + 1, x)
    yield (y - 1, x)
    yield (y, x + 1)
    yield (y, x - 1)


def part_one(data):
    regions = parse(data)
    price = 0
    for region in regions:
        area = len(region)
        perimeter = 0
        for point in region:
            for a in around(point):
                perimeter += a not in region
        price += area * perimeter

    return price


def around_with_direction(point):
    y, x = point

    for d in Direction.cardinal():
        dy, dx = d.value
        yield (y + dy, x + dx), d


def part_two(data):
    regions = parse(data)
    price = 0
    for region in regions:
        area = len(region)
        sides = []
        for point in sorted(region):
            for around, around_direction in around_with_direction(point):
                if around not in region:
                    ay, ax = around
                    match = False
                    for side_direction, points in sides:
                        if side_direction != around_direction:
                            continue
                        for sy, sx in points:
                            if (
                                (
                                    side_direction is Direction.WEST
                                    or side_direction is Direction.EAST
                                )
                                and ax == sx
                                and abs(ay - sy) == 1
                            ):
                                points.add(around)
                                match = True
                                break
                            elif (
                                (
                                    side_direction is Direction.NORTH
                                    or side_direction is Direction.SOUTH
                                )
                                and ay == sy
                                and abs(ax - sx) == 1
                            ):
                                points.add(around)
                                match = True
                                break

                        if match:
                            break
                    else:
                        sides.append((around_direction, set([around])))

        price += area * len(sides)

    return price


print(part_one(data))
print(part_two(data))
