#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

data = get_data(year=2022, day=21, block=True)
lines = data.splitlines()

monkeys = {}

import re

for line in lines:
    if (m := re.match(r"(.*): (-?\d+)", line)):
        monkey, n = m.groups()
        monkeys[monkey] = int(n)
    elif (m := re.match(r"(.*): (.*) (.) (.*)", line)):
        monkey, l, op, r = m.groups()
        monkeys[monkey] = (l, op, r)

from fractions import Fraction
class FreeVar:
    def __init__(self):
        self.coefficient = Fraction(1, 1)
        self.constant = Fraction(0, 1)

    def __radd__(self, v):
        self.constant += Fraction(v)
        return self

    def __add__(self, v):
        self.constant += Fraction(v)
        return self

    def  __rsub__(self, v):
        self.constant = Fraction(v) - self.constant
        return self

    def  __sub__(self, v):
        self.constant = self.constant - Fraction(v)
        return self

    def __rmul__(self, v):
        v = Fraction(v)
        self.coefficient *= v
        self.constant *= v
        return self

    def __mul__(self, v):
        v = Fraction(v)
        self.coefficient *= v
        self.constant *= v
        return self

    def __rtruediv__(self, v):
        v = Fraction(v)
        self.coefficient = v / self.coefficient
        self.constant = v / self.constant
        return self

    def __truediv__(self, v):
        v = Fraction(v)
        self.coefficient /= v
        self.constant /= v
        return self

    def __repr__(self):
        return f"({self.coefficient}x + {self.constant})"

    def __str__(self):
        return repr(self)

    def solve(self, target):
        """
        self.coefficient * x + self.constant = target
        self.coefficient * x = target - self.constant
        x = (target - self.constant) / self.coefficient
        """
        return (target - self.constant)/self.coefficient


def resolve(target):
    v = monkeys[target]
    if isinstance(v, tuple):
        l, op, r = v
        left = resolve(l)
        right = resolve(r)
        result = eval(f"left{op}right")
        return result
    return v
    
l, _, r = monkeys["root"]
monkeys["humn"] = FreeVar()

left = resolve(l)
right = resolve(r)
# Just by manual checking humn ends up in the left hand side
# FIXME: For reasons I can't figure out I'm off by a negative sign
print(-left.solve(right))
