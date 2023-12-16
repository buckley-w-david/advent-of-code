from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Point3 = namedtuple('Point', ['x', 'y', 'z'])

def manhattan_distance(p1: Point, p2: Point):
    return abs(p2.x - p1.x) + abs(p2.y - p1.y)
