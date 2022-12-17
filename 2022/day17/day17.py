#!/usr/bin/env python

from aocd import get_data

raw = get_data(year=2022, day=17, block=True)
data = [-1 if c == "<" else 1 for c in raw]

t = 0

DASH = { (0, 2), (0, 3), (0, 4), (0, 5) }
PLUS = { (0, 3), (1, 2), (1, 3), (1, 4), (2, 3) }
CORNER = { (2, 4), (1, 4), (0, 2), (0, 3), (0, 4) }
BAR = { (0, 2), (1, 2), (2, 2), (3, 2) }
SQUARE = { (0, 2), (0, 3), (1, 2), (1, 3) }

rocks = [DASH, PLUS, CORNER, BAR, SQUARE]

occupied = set()
wind_ptr = 0
rock_ptr = 0

FLOOR = 1

def lift(rock, amt):
    return set((y+amt, x) for (y, x) in rock)

def shift(rock, d):
    return set((y, x+d) for y, x in rock)

def gx(p):
    return p[1]

def display(points):
    s = ''
    print("0123456")
    my = max(points)[0]
    for y in range(my+1):
        for x in range(7):
            if (y, x) in points:
                s += '#'
            else:
                s += ' '
        s += '\n'
    print('\n'.join(s.splitlines()[::-1]))

def collide(rock):
    return occupied.intersection(rock)

goal = 1000000000000
tick = 0

memory = {}
while tick < goal:
    state = (rock_ptr, wind_ptr)
    if state in memory:
        ot, of = memory[state]
        if (goal - tick) % (tick - ot) == 0:
            print(FLOOR - 1 + (goal - tick) // (tick - ot) * (FLOOR - of))
            break
    memory[state] = (tick, FLOOR)
            
    rock = lift(rocks[rock_ptr], FLOOR+3)
    rock_ptr = (rock_ptr + 1) % len(rocks)

    falling = True

    while falling:
        movement = data[wind_ptr]
        wind_ptr = (wind_ptr + 1) % len(data)

        sr = shift(rock, movement)
        if max(sr, key=gx)[1] >= 7 or min(sr, key=gx)[1] < 0 :
            pass
        elif collide(sr):
            pass
        else:
            rock = sr

        lr = lift(rock, -1)
        if collide(lr) or min(lr)[0] <= 0:
            falling = False
        else:
            rock = lr
    FLOOR = max(FLOOR, max(rock)[0]+1)
    clear = 0
    occupied.update(rock)

    tick += 1
