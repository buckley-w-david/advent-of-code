from collections import defaultdict
import re
from aoc_utils import *
from aocd import get_data

data = get_data(year=2018, day=7, block=True)

def parse_dependencies(data):
    dependencies = defaultdict(set)
    for line in data.splitlines():
        if match := re.match(r"Step (\w) must be finished before step (\w) can begin.", line):
            f, s = match.groups()
            dependencies[s].add(f)
            dependencies[f]
    return dependencies

def part_one(data):
    dependencies = parse_dependencies(data)
    ordered = []
    while dependencies:
        next_step = sorted(k for (k, v) in dependencies.items() if not v)[0]
        ordered.append(next_step)
        dependencies.pop(next_step)
        for k in dependencies:
            dependencies[k].discard(next_step)

    return ''.join(ordered)

def work_time(letter):
    return 60 + ord(letter) - ord('A') + 1

MAX_WORKERS = 5
def part_two(data):
    dependencies = parse_dependencies(data)
    workers = [0]*MAX_WORKERS
    work_items = ['']*MAX_WORKERS

    second = 0
    while dependencies or sum(workers) > 0:
        available = sorted(k for (k, v) in dependencies.items() if not v)
        for letter in available:
            for i in range(MAX_WORKERS):
                if workers[i] == 0:
                    workers[i] = work_time(letter)
                    work_items[i] = letter
                    dependencies.pop(letter)
                    break


        for i in range(MAX_WORKERS):
            letter = work_items[i]
            time = workers[i]
            if time == 1:
                for k in dependencies:
                    dependencies[k].discard(letter)
            if workers[i] > 0:
                workers[i] -= 1

        second += 1

    return second

print(part_one(data))
print(part_two(data))
