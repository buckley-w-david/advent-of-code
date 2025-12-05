import re

from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=14, block=True)


def parse(data):
    stats = {}
    for line in data.splitlines():
        m = re.match(
            r"(.*) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.",
            line,
        )
        name, speed, go_time, rest_time = m.groups()
        stats[name] = (int(speed), int(go_time), int(rest_time))

    return stats


def calculate_distances(reindeer_stats, time):
    distances = {}
    for name, stats in reindeer_stats.items():
        total_time = stats[1] + stats[2]
        remainder = time % total_time

        distance = stats[0] * stats[1] * (time // total_time)
        distance += stats[0] * min(remainder, stats[1])
        distances[name] = distance
    return distances


def part_one(data):
    return max(calculate_distances(parse(data), 2503).values())


def part_two(data):
    # I am dissapointed that my guess of what part two would be was wrong
    # I was expecting them to _dramatically_ increase the race time
    # This is why I went out of my way to do calculate distances intelligently
    # instead of simulating the race
    # Now it seems I must simulate the race
    reindeer_stats = parse(data)
    cooldowns = {name: 0 for name in reindeer_stats.keys()}
    distances = {name: 0 for name in reindeer_stats.keys()}
    points = {name: 0 for name in reindeer_stats.keys()}

    t = 2503
    for i in range(1, t + 1):
        for name, stats in reindeer_stats.items():
            if cooldowns[name] > 0:
                cooldowns[name] -= 1
                continue

            if i % (stats[1] + stats[2]) == stats[1]:
                cooldowns[name] = stats[2]

            distances[name] += stats[0]

        md = max(distances.values())
        for name, distance in distances.items():
            if distance == md:
                points[name] += 1

    return max(points.values())


print(part_one(data))
print(part_two(data))
