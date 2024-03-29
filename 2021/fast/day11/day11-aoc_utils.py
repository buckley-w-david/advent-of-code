#!/usr/bin/env python

from aocd import get_data
from aoc_utils import Grid

data = get_data(year=2021, day=11, block=True)

class Oct:
    def __init__(self, n):
        self.n = n
        self.flashed = False
        self.flash_count = 0

    def bump(self):
        self.n += 1

    def emit(self):
        if self.n > 9 and not self.flashed:
            self.flash_count += 1
            self.flashed = True
            return True
        return False

    def reset(self):
        if self.n > 9:
            self.n = 0
        self.flashed = False

    def __repr__(self):
        return str(self.n)

    def __str__(self):
        return str(self.n)

lines = [[Oct(int(c)) for c in l] for l in data.split("\n")]
grid = Grid(lines)

def process_flash(yx):
    for (yx, oct) in grid.around_with_index(yx):
        oct.bump()
        if oct.emit():
            process_flash(yx)

gen = 0
all_flashed = False
while not all_flashed:
    gen += 1
    grid.apply(Oct.bump)

    for (yx, oct) in grid.row_major_with_index():
        if oct.emit():
            process_flash(yx)

    all_flashed = all([oct.flashed for oct in grid.row_major()])
    grid.apply(Oct.reset)

print(gen)
