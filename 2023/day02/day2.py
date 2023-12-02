import re

from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=2, block=True)

games = {}
for line in data.splitlines():
    ids, gs = line.split(":")
    id = int(re.search(r"Game (\d+)", ids).group(1))

    pulls = gs.strip().split(";")
    games[id] = [[0, 0, 0] for _ in range(len(pulls))]
    for i, pull in enumerate(pulls):
        if red := re.search(r"(\d+) red", pull):
            games[id][i][0] = int(red.group(1))
        if green := re.search(r"(\d+) green", pull):
            games[id][i][1] = int(green.group(1))
        if blue := re.search(r"(\d+) blue", pull):
            games[id][i][2] = int(blue.group(1))

LIMIT = RED_LIMIT, GREEN_LIMIT, BLUE_LIMIT = 12, 13, 14
def part_one(games):
    total = 0
    for id, pulls in games.items():
        for r, g, b in pulls:
            if r > RED_LIMIT:
                break
            elif g > GREEN_LIMIT:
                break
            elif b > BLUE_LIMIT:
                break
        else:
            total += id
    return total

def part_two(games):
    total = 0
    for _, pulls in games.items():
        mr, mg, mb = 0, 0, 0
        for r, g, b in pulls:
            mr = max(mr, r)
            mg = max(mg, g)
            mb = max(mb, b)
        total += mr*mg*mb
    return total

print(part_one(games))
print(part_two(games))
