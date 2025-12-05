import re

from aoc_utils import *
from aocd import get_data

from functools import cache

data = get_data(year=2015, day=7, block=True)


def identity(l, _):
    return l


def negate(l, _):
    return ~l


def and_(l, r):
    return l & r


def or_(l, r):
    return l | r


def lshift(l, r):
    return l << r


def rshift(l, r):
    return l >> r


VTABLE = {
    "NOT": negate,
    "AND": and_,
    "OR": or_,
    "LSHIFT": lshift,
    "RSHIFT": rshift,
    "IDENTITY": identity,
}


def parse_circuit(data):
    circuit = {}
    for line in data.splitlines():
        l, op, r, out = None, None, None, None
        if m := re.match(r"(.*) (.*) (.*) -> (.*)", line):
            l, op, r, out = m.groups()
        elif m := re.match(r"NOT (.*) -> (.*)", line):
            op = "NOT"
            l, out = m.groups()
        elif m := re.match(r"(.*) -> (.*)", line):
            op = "IDENTITY"
            l, out = m.groups()
        else:
            assert False

        if l.isdigit():
            l = int(l)

        if r and r.isdigit():
            r = int(r)

        circuit[out] = (l, op, r)
    return circuit


def part_one(data):
    circuit = parse_circuit(data)

    @cache
    def eval(wire):
        l, op, r = wire
        if not isinstance(l, int):
            l = eval(circuit[l])
        if r and not isinstance(r, int):
            r = eval(circuit[r])

        r = VTABLE[op](l, r)
        return r % 65536

    return eval(circuit["a"])


def part_two(data):
    circuit = parse_circuit(data)

    @cache
    def eval(wire):
        l, op, r = wire
        if not isinstance(l, int):
            l = eval(circuit[l])
        if r and not isinstance(r, int):
            r = eval(circuit[r])

        r = VTABLE[op](l, r)
        return r % 65536

    circuit["b"] = (eval(circuit["a"]), "IDENTITY", None)
    eval.cache_clear()
    return eval(circuit["a"])


print(part_one(data))
print(part_two(data))
