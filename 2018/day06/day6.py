from collections import defaultdict
from aoc_utils import *
from aocd import get_data

data = get_data(year=2018, day=6, block=True)

def closest_without_tie(points, point):
    distances = { p: manhattan_distance(p, point) for p in points }
    in_distance_order = sorted(distances, key=distances.get) # type: ignore
    if distances[in_distance_order[0]] != distances[in_distance_order[1]]:
        return in_distance_order[0]

def part_one(data):
    points = { Point(*ints(l)) for l in data.splitlines() }
    bbox_xmin = min(points).x
    bbox_xmax = max(points).x

    bbox_ymin = min(points, key=lambda p: p.y).y
    bbox_ymax = max(points, key=lambda p: p.y).y

    infinite_areas = set()

    for y in range(bbox_ymin-1, bbox_ymax+2):
        for x in [bbox_xmin-1, bbox_xmax+1]:
            outside = Point(x, y)
            closest = closest_without_tie(points, outside)
            if closest:
                infinite_areas.add(closest)

    for x in range(bbox_xmin-1, bbox_xmax+2):
        for y in [bbox_ymin-1, bbox_ymax+1]:
            outside = Point(x, y)
            closest = closest_without_tie(points, outside)
            if closest:
                infinite_areas.add(closest)

    area = defaultdict(int)
    for y in range(bbox_ymin, bbox_ymax+1):
        for x in range(bbox_xmin, bbox_xmax+1):
            p = Point(x, y)
            closest = closest_without_tie(points, p)
            if closest:
                area[closest] += 1

    for p in infinite_areas:
        area.pop(p)

    return max(area.values())

# This is _really_ slow
# but it does work
# I feel like I've missed some connection with the approach from part 1
def part_two(data):
    points = { Point(*ints(l)) for l in data.splitlines() }
    point = points.pop()
    points.add(point)

    max_distance = 10_000
    area = 0
    for dy in range(-max_distance, max_distance):
        for dx in range(abs(dy)-max_distance, -(abs(dy)-max_distance)+1):
            candidate = Point(point.x+dx, point.y+dy)
            td = sum(map(lambda p: manhattan_distance(candidate, p), points))
            if td < max_distance:
                area += 1
    return area

print(part_one(data))
# print(part_two(data))
