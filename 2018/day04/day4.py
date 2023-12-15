from collections import defaultdict
import re
from aoc_utils import *
from aocd import get_data

data = get_data(year=2018, day=4, block=True)

def track_sleep(data):
    guard = -1
    sleep_minute, wake_minute = 0, 0
    sleep_tracker = defaultdict(lambda : defaultdict(int))
    for event in sorted(data.strip().splitlines()):
        if match := re.match(r"\[\d\d\d\d-\d\d-\d\d \d\d:(\d\d)\] Guard #(\d+) begins shift", event):
            guard = int(match.group(2))
        elif match := re.match(r"\[\d\d\d\d-\d\d-\d\d \d\d:(\d\d)\] falls asleep", event):
            sleep_minute = int(match.group(1))
        elif match := re.match(r"\[\d\d\d\d-\d\d-\d\d \d\d:(\d\d)\] wakes up", event):
            wake_minute = int(match.group(1))
            for m in range(sleep_minute, wake_minute):
                sleep_tracker[guard][m] += 1
    return sleep_tracker

def part_one(data):
    sleep_tracker = track_sleep(data)
    sleepy_guard = max(sleep_tracker, key=lambda g: sum(sleep_tracker[g].values()))
    sleepy_minute = max(sleep_tracker[sleepy_guard], key=lambda m: sleep_tracker[sleepy_guard][m])
    return sleepy_guard*sleepy_minute

def part_two(data):
    sleep_tracker = track_sleep(data)
    sleepy_guard = max(sleep_tracker, key=lambda g: max(sleep_tracker[g].values()))
    sleepy_minute = max(sleep_tracker[sleepy_guard], key=lambda m: sleep_tracker[sleepy_guard][m])
    return sleepy_guard*sleepy_minute

print(part_one(data))
print(part_two(data))
