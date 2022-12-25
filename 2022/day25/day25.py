#!/usr/bin/env python

from aoc_utils import * # type: ignore

from aocd import get_data

data = get_data(year=2022, day=25, block=True)
lines = data.splitlines()

s = 0
digits = {
  '2': 2,
  '1': 1,
  '0': 0,
  '-': -1,
  '=': -2,
}
rd = {
  2: '2',
  1: '1',
  0 : '0',
  -1: '-',
  -2: '=',
}

for line in lines:
    l = len(line)-1
    n = 0
    for i, c in enumerate(line):
        n += (5 ** (l-i)) * digits[c]
    s += n

n = ''
while s:
    d = ((s + 2) % 5) - 2
    n += rd[d]
    s -= d
    s //= 5
print(''.join(reversed(n)))
