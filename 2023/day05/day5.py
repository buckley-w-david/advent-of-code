from collections import defaultdict
import re
from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=5, block=True)
blocks = data.split("\n\n")

seeds = ints(blocks[0])

mappings = defaultdict(dict)

steps = []
for block in blocks[1:]:
    lines = block.splitlines()
    conversion = re.match(r"(.*)-to-(.*) map:", lines[0])
    steps.append((conversion.group(1), conversion.group(2)))

    mapping = {}
    for line in lines[1:]:
        dst_start, src_start, length = ints(line)
        mapping[(src_start, src_start+length)] = (dst_start, dst_start+length)
    mappings[conversion.group(1)][conversion.group(2)] = mapping

def part_one(seeds, mappings):
    seeds = seeds[:]
    for i in range(len(seeds)):
        for src, dst in steps:
            ranges = mappings[src][dst]
            for (ss, se), (ds, _) in ranges.items():
                if ss <= seeds[i] < se:
                    v =  ds + (seeds[i] - ss)
                    seeds[i] = v
                    break
    return min(seeds)

def non_negative_integers():
    n = 0
    while True:
        yield n
        n += 1

def find_source_for_destination(mapping, destination: int):
    for (ss, _), (ds, de) in mapping.items():
        if ds <= destination < de:
            return ss + (destination - ds)

def part_two(seeds, mappings):
    seed_ranges = [(seeds[i], seeds[i]+seeds[i+1]) for i in range(0, len(seeds), 2)]
    for location in non_negative_integers():
        target = location
        for (src, dst) in reversed(steps):
            n = find_source_for_destination(mappings[src][dst], target)
            if n is not None: target  = n

        for (seed_start, seed_end) in seed_ranges:
            if seed_start <= target < seed_end:
                return location

print(part_one(seeds, mappings))
print(part_two(seeds, mappings))
