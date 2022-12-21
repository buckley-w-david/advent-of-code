#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data
from sympy.polys.specialpolys import w_polys

data = get_data(year=2022, day=21, block=True)
data = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
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
    def __init__(self, coefficient=Fraction(1), constant=Fraction(0)):
        self.coefficient = coefficient
        self.constant = constant

    def __radd__(self, v):
        return FreeVar(self.coefficient, self.constant+Fraction(v))

    def __add__(self, v):
        return FreeVar(self.coefficient, self.constant+Fraction(v))

    def  __rsub__(self, v):
        return FreeVar(self.coefficient, Fraction(v) - self.constant)

    def  __sub__(self, v):
        return FreeVar(self.coefficient, self.constant - Fraction(v))

    def __rmul__(self, v):
        v = Fraction(v)
        return FreeVar(self.coefficient * v, self.constant * v)

    def __mul__(self, v):
        v = Fraction(v)
        return FreeVar(self.coefficient * v, self.constant * v)

    # FIXME: This method is very wrong
    def __rtruediv__(self, v):
        v = Fraction(v)
        return FreeVar(v / self.coefficient, v / self.constant)

    def __truediv__(self, v):
        v = Fraction(v)
        return FreeVar(self.coefficient / v, self.constant / v)

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
print(left.solve(right))
