from functools import total_ordering
from dataclasses import dataclass

with open("input.txt", "r") as f:
    data = f.read()


@dataclass
@total_ordering
class Range:
    left: int
    right: int

    def __contains__(self, x: int) -> bool:
        return x >= self.left and x <= self.right

    def __len__(self):
        return self.right - self.left + 1

    def __lt__(self, other):
        return self.left < other.left

    def covers(self, other: "Range") -> bool:
        assert self.left <= other.left
        return self.left <= other.left and self.right >= other.right

    def intersects(self, other: "Range") -> bool:
        assert self.left <= other.left
        return self.left <= other.left and self.right >= other.left


def parse(data):
    range_lines, id_lines = data.split("\n\n")
    ranges = []
    for line in range_lines.splitlines():
        left, right = line.split("-")
        ranges.append(Range(left=int(left), right=int(right)))

    ids = []
    for line in id_lines.splitlines():
        ids.append(int(line))

    return ranges, ids


def part_one(data):
    ranges, ids = parse(data)
    count = 0
    for id in ids:
        # O(n**2) is only bad if you have lots of data :upside_down_face:
        for r in ranges:
            if id in r:
                count += 1
                break
    return count


def part_two(data):
    ranges, _ = parse(data)
    ranges.sort()
    merged = [ranges[0]]
    for next_range in ranges[1:]:
        current_range = merged[-1]
        if current_range.covers(next_range):
            continue
        elif current_range.intersects(next_range):
            merged[-1] = Range(left=current_range.left, right=next_range.right)
        else:
            merged.append(next_range)
    return sum(len(r) for r in merged)


print(part_one(data))
print(part_two(data))
