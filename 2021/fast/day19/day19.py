#!/usr/bin/env python

from aocd import get_data

data = get_data(year=2021, day=19, block=True)

# Assumption: Distrubtion patterns of beacons are globally unique

class Scanner:
    def __init__(self, points):
        self.points = points

    # I don't know 3d stuff well enough, this is more than 24 permutations
    def point_permutations(self):
        yield {(p[0], p[1], p[2]) for p in self.points}
        yield {(p[0], p[2], p[1]) for p in self.points}
        yield {(p[1], p[0], p[2]) for p in self.points}
        yield {(p[1], p[2], p[0]) for p in self.points}
        yield {(p[2], p[0], p[1]) for p in self.points}
        yield {(p[2], p[1], p[0]) for p in self.points}

        yield {(-p[0], -p[1], -p[2]) for p in self.points}
        yield {(-p[0], -p[2], -p[1]) for p in self.points}
        yield {(-p[1], -p[0], -p[2]) for p in self.points}
        yield {(-p[1], -p[2], -p[0]) for p in self.points}
        yield {(-p[2], -p[0], -p[1]) for p in self.points}
        yield {(-p[2], -p[1], -p[0]) for p in self.points}

        yield {(p[0], -p[1], -p[2]) for p in self.points}
        yield {(p[0], -p[2], -p[1]) for p in self.points}
        yield {(p[1], -p[0], -p[2]) for p in self.points}
        yield {(p[1], -p[2], -p[0]) for p in self.points}
        yield {(p[2], -p[0], -p[1]) for p in self.points}
        yield {(p[2], -p[1], -p[0]) for p in self.points}

        yield {(-p[0], p[1], -p[2]) for p in self.points}
        yield {(-p[0], p[2], -p[1]) for p in self.points}
        yield {(-p[1], p[0], -p[2]) for p in self.points}
        yield {(-p[1], p[2], -p[0]) for p in self.points}
        yield {(-p[2], p[0], -p[1]) for p in self.points}
        yield {(-p[2], p[1], -p[0]) for p in self.points}

        yield {(-p[0], -p[1], p[2]) for p in self.points}
        yield {(-p[0], -p[2], p[1]) for p in self.points}
        yield {(-p[1], -p[0], p[2]) for p in self.points}
        yield {(-p[1], -p[2], p[0]) for p in self.points}
        yield {(-p[2], -p[0], p[1]) for p in self.points}
        yield {(-p[2], -p[1], p[0]) for p in self.points}

        yield {(-p[0], p[1], p[2]) for p in self.points}
        yield {(-p[0], p[2], p[1]) for p in self.points}
        yield {(-p[1], p[0], p[2]) for p in self.points}
        yield {(-p[1], p[2], p[0]) for p in self.points}
        yield {(-p[2], p[0], p[1]) for p in self.points}
        yield {(-p[2], p[1], p[0]) for p in self.points}

        yield {(p[0], -p[1], p[2]) for p in self.points}
        yield {(p[0], -p[2], p[1]) for p in self.points}
        yield {(p[1], -p[0], p[2]) for p in self.points}
        yield {(p[1], -p[2], p[0]) for p in self.points}
        yield {(p[2], -p[0], p[1]) for p in self.points}
        yield {(p[2], -p[1], p[0]) for p in self.points}

        yield {(p[0], p[1], -p[2]) for p in self.points}
        yield {(p[0], p[2], -p[1]) for p in self.points}
        yield {(p[1], p[0], -p[2]) for p in self.points}
        yield {(p[1], p[2], -p[0]) for p in self.points}
        yield {(p[2], p[0], -p[1]) for p in self.points}
        yield {(p[2], p[1], -p[0]) for p in self.points}

    @staticmethod
    def parse(s):
        lines = s.splitlines()
        points = []
        for line in lines[1:]:
            points.append(tuple(map(int, line.split(','))))
        return Scanner(points)

scanners = []
for pl in data.split('\n\n'):
    lines = pl.splitlines()
    points = []
    for line in lines[1:]:
        points.append(tuple(map(int, line.split(','))))
    scanners.append(Scanner(set(points)))

baseline = scanners.pop(0).points

def find_overlapping_coordinates(baseline):
    for scanner in scanners:
        for permutation in scanner.point_permutations():
            for baseline_point in baseline:
                bx, by, bz = baseline_point
                for permutation_point in permutation:
                    px, py, pz = permutation_point
                    x_offset = bx-px
                    y_offset = by-py
                    z_offset = bz-pz

                    matches = 1
                    # As brute force as you can possibly make it...
                    # For every point in every permutation compare it against every point in the set of already known points.
                    # If the offset generated by that permutation point applied to the other points in this permutation give us 12 hits
                    # Then we have a match
                    for mapped_point in permutation:
                        x, y, z = mapped_point
                        if (x+x_offset, y+y_offset, z+z_offset) in baseline:
                            matches += 1
                        if matches >= 12:
                            return scanner, {(x+x_offset, y+y_offset, z+z_offset) for x, y, z in permutation}, (x_offset, y_offset, z_offset)

scanner_positions = [(0, 0, 0)]
while scanners:
    print(len(scanners))
    s, points, offsets = find_overlapping_coordinates(baseline)
    scanner_positions.append(offsets)
    print(points)
    scanners.remove(s)
    baseline.update(points)
print(baseline)
print(len(baseline))
print(scanner_positions)

md = -1
for s1 in scanner_positions:
    a1, b1, c1 = s1
    for s2 in scanner_positions:
        a2, b2, c2 = s2
        md = max(md, (a1-a2)+(b1-b2)+(c1-c2))
print(md)
