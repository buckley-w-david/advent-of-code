import re
from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=6, block=True)

def part_one(data):
    t, d = data.splitlines()
    times = ints(t)
    distances = ints(d)
    races = zip(times, distances)

    margin = 1
    for time, distance in races:
        better = 0
        for speed in range(time):
            my_distance = speed*(time-speed)
            better += my_distance > distance
        margin *= better
    return margin

def part_two(data):
    t, d = data.splitlines()
    time = int(''.join(re.findall(r"\d", t)))
    distance = int(''.join(re.findall(r"\d", d)))
    better = 0
    for speed in range(time):
        my_distance = speed*(time-speed)
        better += my_distance > distance
    return better

print(part_one(data))
print(part_two(data))
