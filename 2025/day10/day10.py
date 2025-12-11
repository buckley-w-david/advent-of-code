from collections import deque
import re
import string

from aocd import get_data
import z3

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


def parse_two(data):
    pattern = re.compile(r"\[([.#]+)] ((?:\([\d,]+\) )+){([\d,]+)}")
    r = []
    for line in data.splitlines():
        m = pattern.match(line)
        assert m

        button_groups = m.group(2).strip()
        joltage_group = m.group(3).strip()

        joltage = tuple(int(n) for n in joltage_group.split(","))

        buttons = []
        for m in re.findall(r"\(([\d,]+)\)", button_groups):
            l = [0 for _ in range(len(joltage))]
            for c in m.split(","):
                l[int(c)] = 1
            buttons.append(tuple(l))

        r.append((buttons, joltage))

    return r


def min_joltage_length(joltage, buttons):
    # Coefficients for each of the buttons
    coefficients = [z3.Int(string.ascii_lowercase[i]) for i in range(len(buttons))]
    solver = z3.Optimize()
    # You can't press a button a negative number of times
    for c in coefficients:
        solver.add(c >= 0)

    for counter in range(len(joltage)):
        solver.add(
            # The sum of all button values multiplied by their coefficient in each dimension of the answer
            # must equal the final joltage number in that dimension
            z3.Sum(coefficients[i] * buttons[i][counter] for i in range(len(buttons)))
            == joltage[counter]
        )

    _obj = solver.minimize(z3.Sum(coefficients))
    if solver.check() == z3.sat:
        model = solver.model()
        return sum(model[c].as_long() for c in coefficients)
    else:
        assert False


def part_two(data):
    return sum(
        min_joltage_length(joltage, buttons) for buttons, joltage in parse_two(data)
    )


print(part_one(data))
print(part_two(data))
