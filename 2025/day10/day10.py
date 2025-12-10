from collections import deque
import re
from aocd import get_data

data = get_data(year=2025, day=10, block=True)


def parse(data):
    pattern = re.compile(r"\[([.#]+)] ((?:\([\d,]+\) )+){([\d,]+)}")
    r = []
    for line in data.splitlines():
        m = pattern.match(line)
        assert m

        diagram = m.group(1).strip()
        button_groups = m.group(2).strip()
        joltage_group = m.group(3).strip()

        size = len(diagram)
        dn = 0
        for i, c in enumerate(diagram):
            if c == "#":
                dn |= 2 ** (size - i - 1)

        buttons = []
        for m in re.findall(r"\(([\d,]+)\)", button_groups):
            bn = 0
            for c in m.split(","):
                bn |= 2 ** (size - int(c) - 1)
            buttons.append(bn)

        joltage = tuple(int(n) for n in joltage_group.split(","))

        r.append((dn, buttons, joltage))

    return r


def min_sequence_length(target, buttons):
    seen = {0}
    lights = deque([(0, 0)])
    while True:
        current, depth = lights.popleft()
        for button in buttons:
            v = current ^ button
            if v == target:
                return depth + 1
            elif v not in seen:
                seen.add(v)
                lights.append((v, depth + 1))


def part_one(data):
    return sum(
        min_sequence_length(target, buttons) for target, buttons, _ in parse(data)
    )


def part_two(data):
    return parse(data)


print(part_one(data))
print(part_two(data))
