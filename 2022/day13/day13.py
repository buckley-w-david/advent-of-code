#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

from ast import literal_eval

data = get_data(year=2022, day=13, block=True)

lines = [literal_eval(line) for line in (data.splitlines() + ["[[2]]","[[6]]"]) if line.strip()]

from itertools import zip_longest

def cmp(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None
    elif isinstance(left, list) and isinstance(right, list):
        for l, r in zip_longest(left, right):
            if l == None:
                return True
            elif r == None:
                return False
            ordered = cmp(l, r)
            if ordered == True:
                return True
            elif ordered == False:
                return False
        return None
    elif isinstance(left, int):
        return cmp([left], right)
    else:
        return cmp(left, [right])

from functools import total_ordering

@total_ordering
class Line:
    def __init__(self, l):
        self.l = l

    def __eq__(self, other):
        return False
    
    def __lt__(self, other):
        return cmp(self.l, other.l)

s = [str(l.l) for l in sorted(map(Line, lines))]
t1 = s.index("[[2]]")+1
t2 = s.index("[[6]]")+1
print(t1*t2)
