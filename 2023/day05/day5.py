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


"""
# Part 2 plan
The numbers are too large to actually forward calculate from seeds to location

Instead calculate backwards from the min location to the seeds to find what seed is needed to get that.
It is unlikely any seed exactly hits the minimum (which is 0), so we will have to keep track of ranges.

The min is either the smallest value that hits the lowest range in location, or the smallest value in an earlier
mapping that misses a later mapping (and so carries through)
"""
