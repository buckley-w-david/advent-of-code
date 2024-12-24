import re

from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=24, block=True)

initial, connections = data.split("\n\n")

wires = {}
states = {}
outputs = []
for line in connections.splitlines():
    m = re.match(r"(.*) (AND|OR|XOR) (.*) -> (.*)", line)
    a, op, b, out = m.groups()
    wires[out] = (a, op, b)
    if out[0] == "z":
        outputs.append(out)
outputs = sorted(outputs)
for line in initial.splitlines():
    m = re.match(r"(.*): (\d+)", line)
    out, val = m.groups()
    states[out] = int(val)

for s in states:
    wires[s] = s


VTABLE = {
    "AND": lambda a, b: a and b,
    "OR": lambda a, b: a or b,
    "XOR": lambda a, b: a ^ b,
}


def expand(wire):
    a, op, b = wires[wire]
    if a[0] != "x" and a[0] != "y":
        a = f"({expand(a)})"
    if b[0] != "x" and b[0] != "y":
        b = f"({expand(b)})"
    return f"{a} {op} {b}"


def validate_carry(wire, idx):
    # These validation methods are _terrible_
    if idx == 0:
        return True

    a, op, b = wires[wire]
    if op != "OR":
        print(wire, idx, "was a bad carry => not OR")
        return False

    aa, bb = a, b
    carry = aa
    if a[0] != "x" and a[0] != "y":
        aa = expand(a)
    if b[0] != "x" and b[0] != "y":
        bb = expand(b)

    carry = None
    if aa == "y%02d AND x%02d" % (idx, idx) or aa == "x%02d AND y%02d" % (idx, idx):
        carry = b
    else:
        carry = a

    if not (
        aa == "y%02d AND x%02d" % (idx, idx)
        or aa == "x%02d AND y%02d" % (idx, idx)
        or bb == "y%02d AND x%02d" % (idx, idx)
        or bb == "x%02d AND y%02d" % (idx, idx)
    ):
        print(wire, idx, f"was a bad carry => no carry from {idx}")
        return False

    a, op, b = wires[carry]
    if op != "AND":
        print(carry, idx, "was a bad carry => no AND")
        return False

    carry = aa
    if a[0] != "x" and a[0] != "y":
        aa = expand(a)
    if b[0] != "x" and b[0] != "y":
        bb = expand(b)

    carry = None
    if aa == "y%02d XOR x%02d" % (idx, idx) or aa == "x%02d XOR y%02d" % (idx, idx):
        carry = b
    else:
        carry = a

    if not (
        aa == "y%02d XOR x%02d" % (idx, idx)
        or aa == "x%02d XOR y%02d" % (idx, idx)
        or bb == "y%02d XOR x%02d" % (idx, idx)
        or bb == "x%02d XOR y%02d" % (idx, idx)
    ):
        print(carry, idx, "was a bad carry => no XOR")
        return False

    return validate_carry(carry, idx - 1)


def validate_output(out, idx):
    a, op, b = wires[out]
    if op != "XOR":
        print(out, "was bad output => no XOR")
        return False

    aa, bb = a, b
    carry = aa
    if a[0] != "x" and a[0] != "y":
        aa = expand(a)
    if b[0] != "x" and b[0] != "y":
        bb = expand(b)

    carry = None
    if aa == "y%02d XOR x%02d" % (idx, idx) or aa == "x%02d XOR y%02d" % (idx, idx):
        carry = b
    else:
        carry = a

    if not (
        aa == "y%02d XOR x%02d" % (idx, idx)
        or aa == "x%02d XOR y%02d" % (idx, idx)
        or bb == "y%02d XOR x%02d" % (idx, idx)
        or bb == "x%02d XOR y%02d" % (idx, idx)
    ):
        print(out, "was bad output => no XOR 2")
        return False

    return validate_carry(carry, idx - 1)


def part_two(_):
    swaps = [
        "qdg",
        "z12",
        "vvf",
        "z19",
        "dck",
        "fgn",
        "nvh",
        "z37",
    ]
    return ",".join(sorted(swaps))

    # These swaps were determined "manually"
    # This was done using the validation code above, visual inspection, and ad-hoc code that has since been removed

    wires["qdg"], wires["z12"] = wires["z12"], wires["qdg"]
    wires["vvf"], wires["z19"] = wires["z19"], wires["vvf"]

    wires["dck"], wires["fgn"] = wires["fgn"], wires["dck"]
    wires["nvh"], wires["z37"] = wires["z37"], wires["nvh"]

    for w in outputs[1:-1]:
        idx = int(w[1:])
        if not validate_output(w, idx):
            breakpoint()
            print(w)


def part_one(_):
    while True:
        any = False
        for out, (a, op, b) in wires.items():
            if out not in states and a in states and b in states:
                states[out] = VTABLE[op](states[a], states[b])
                any = True
        if not any:
            break

    return sum([states[out] * 2**i for i, out in enumerate(sorted(outputs))])


print(part_one(data))
print(part_two(data))
