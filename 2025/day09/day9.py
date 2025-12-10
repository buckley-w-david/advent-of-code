from collections import defaultdict
import itertools

from aocd import get_data

data = get_data(year=2025, day=9, block=True)


def parse(data):
    return [tuple(int(n) for n in line.split(",")) for line in data.splitlines()]


def area(a, b):
    x1, y1 = a
    x2, y2 = b
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    return width * height


def part_one(data):
    red_tiles = parse(data)
    return max(area(a, b) for a, b in itertools.combinations(red_tiles, 2))


# This isn't great
def part_two(data):
    red_tiles = parse(data)

    boundary = set()
    intersections = defaultdict(set)
    for i in range(len(red_tiles)):
        (x1, y1), (x2, y2) = red_tiles[i], red_tiles[(i + 1) % len(red_tiles)]
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                boundary.add((x1, y))
                if y != min(y1, y2):
                    intersections[y].add(x1)
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                boundary.add((x, y1))
        else:
            assert False

    def interior_or_boundary(x, y):
        # I would prefer not to special case the boundary points... Alas
        if (x, y) in boundary:
            return True

        s = 0

        # Upon inspection of the actual data, this isn't a great way to check for intersections
        # Nearly all y coordinates have exactly two intersections
        # The whole thing forms a giant sphere with a slice
        # You could probably leverage knowledge about the geometry for a faster solution, but I prefer to keep it general
        for xi in intersections[y]:
            if x >= xi:
                s += 1
        return s % 2 == 1

    max_area = None
    # I can't think of any good criteria to use for candidate selection other than just exhaustively enumerating possibilities
    # but surely there's just some trick I'm not thinking of
    for a, b in itertools.combinations(red_tiles, 2):
        # I think it's safe to assume that the maximal rectangle isn't length 1 in one of its dimensions
        if a[0] == b[0] or a[1] == b[1]:
            continue

        (x1, y1), (x2, y2) = a, b

        # The rectangle is valid if all points along its perimeter are on the boundary or interior
        # This seems like a pretty terrible approach, but it's the best I came up with
        # Even with this strategy there should be some nice way to save a lot of effectively duplicate work
        # While checking if (x, y) is interior, we should learn a lot about nearby points as well (like x +/- 1, y)
        all_interior = True
        lower, upper = min(x1, x2), max(x1, x2)
        for x in range(lower, upper + 1):
            all_interior &= interior_or_boundary(x, y1)
            if not all_interior:
                break

            all_interior &= interior_or_boundary(x, y2)
            if not all_interior:
                break

        if not all_interior:
            continue

        lower, upper = min(y1, y2), max(y1, y2)
        for y in range(lower, upper + 1):
            all_interior &= interior_or_boundary(x1, y)
            if not all_interior:
                break

            all_interior &= interior_or_boundary(x2, y)
            if not all_interior:
                break

        if not all_interior:
            continue

        aa = area(a, b)
        if max_area is None or aa > max_area:
            max_area = aa

    return max_area


print(part_one(data))
print(part_two(data))
