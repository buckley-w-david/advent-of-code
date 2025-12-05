from collections import defaultdict
import re
from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=5, block=True)

Transformation = tuple[range, int]

def parse_line(line: str) -> Transformation:
    dst_start, src_start, length = ints(line)
    return range(src_start, src_start+length), dst_start - src_start

def parse_map(block: str) -> list[Transformation]:
    return [
        parse_line(line) for line in block.splitlines()[1:]
    ]

def apply_map(map: list[Transformation], value: int) -> int:
    for (range, offset) in map:
        if value in range:
            return value+offset
    return value

def part_one(data):
    blocks = data.split("\n\n")
    seeds = ints(blocks[0])
    maps = [parse_map(block) for block in blocks[1:]]
    values = []
    for seed in seeds:
        value = seed
        for map in maps:
            value = apply_map(map, value)
        values.append(value)
    return min(values)



def collapse_maps(m1, m2):
    new_ranges = []
    for (r2, t2) in m2:
        for (r1, t1) in m1:
            if r2.start - t1 < r1.stop and r2.stop - t1 >= r1.start:
                low_point = r2.start - t1
                high_point = r2.stop - t1
                if low_point <= r1.start:
                    if high_point > r1.stop:
                        new_ranges.append((r1, t1+t2))
                    else:
                        new_ranges.extend([
                            (range(r1.start, high_point), t1+t2),
                            (range(high_point, r1.stop), t1),
                        ])
                else:
                    if high_point > r1.stop:
                        new_ranges.extend([
                            (range(r1.start, low_point), t1),
                            (range(low_point, r1.stop), t1+t2)
                        ])
                    else:
                        new_ranges.extend([
                            (range(r1.start, low_point), t1),
                            (range(low_point, high_point), t1+t2),
                            (range(high_point, r1.stop), t1)
                        ])
    return new_ranges



def part_two(data):
    blocks = data.split("\n\n")
    seeds = ints(blocks[0])
    maps = [parse_map(block) for block in blocks[1:]]
    merged_map = maps[0]
    for map in maps[1:]:
        merged_map = collapse_maps(merged_map, map)

    values = []
    for seed in seeds:
        values.append(apply_map(merged_map, seed))
    return min(values)


# def non_negative_integers():
    # n = 0
    # while True:
        # yield n
        # n += 1

# def find_source_for_destination(mapping, destination: int):
    # for (ss, _), (ds, de) in mapping.items():
        # if ds <= destination < de:
            # return ss + (destination - ds)

# def part_two(seeds, mappings):
    # seed_ranges = [(seeds[i], seeds[i]+seeds[i+1]) for i in range(0, len(seeds), 2)]
    # for location in non_negative_integers():
        # target = location
        # for (src, dst) in reversed(steps):
            # n = find_source_for_destination(mappings[src][dst], target)
            # if n is not None: target  = n

        # for (seed_start, seed_end) in seed_ranges:
            # if seed_start <= target < seed_end:
                # return location

# print(part_one(data))
print(part_two(data))
