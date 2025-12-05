from collections import Counter, defaultdict
from itertools import combinations, pairwise
from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=5, block=True)

VOWELS = set("aeiou")
DENY = set(["ab", "cd", "pq", "xy"])


def nice(s, min_vowels=3):
    vowels = 0
    consecutive = False

    last = ""
    for c in s:
        if last + c in DENY:
            return False
        vowels += c in VOWELS
        consecutive |= last == c
        last = c
    return vowels >= min_vowels and consecutive


assert nice("ugknbfddgicrmopn")
assert nice("aaa")
assert not nice("jchzalrnumimnmhp")
assert not nice("haegwjzuvuyypxyu")
assert not nice("dvszwmarrgswjxmb")


def nice_two(s):
    pairs = defaultdict(list)

    for i, (a, b) in enumerate(pairwise(s)):
        pairs[(a, b)].append(i)

    double_pair = False
    for idxs in pairs.values():
        for a, b in combinations(idxs, r=2):
            if (b - a) > 1:
                double_pair = True
                break
        if double_pair:
            break

    if not double_pair:
        return False

    for i in range(len(s) - 2):
        a, b, c = s[i : i + 3]

        if a == c:
            return True

    return False


assert nice_two("qjhvhtzxzqqjkmpb")
assert nice_two("xxyxx")
assert not nice_two("uurcxstgmygtbstg")
assert not nice_two("ieodomkazucvgmuy")


def part_one(data):
    total = 0
    for line in data.splitlines():
        total += nice(line)
    return total


def part_two(data):
    total = 0
    for line in data.splitlines():
        total += nice_two(line)
    return total


print(part_one(data))
print(part_two(data))
