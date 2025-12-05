serial_number = 4172

def power(x, y):
    rack_id = (x + 1) + 10
    power = rack_id * (y+1)
    power += serial_number
    power *= rack_id
    power = (power // 100) % 10
    power -= 5
    return power

def part_one():
    fuel_cells = [[0 for _ in range(300)] for _ in range(300)]
    for y in range(300):
        for x in range(300):
            fuel_cells[y][x] = power(x, y)

    max_fuel = -float('inf')
    max_fuel_loc = (-1, -1)
    for y in range(0, 298):
        for x in range(0, 298):
            s = 0
            for i in range(3):
                for j in range(3):
                    s += fuel_cells[y+i][x+j]
            if s > max_fuel:
                max_fuel = s
                max_fuel_loc = (x+1, y+1)

    return max_fuel_loc

# Very slow
def part_two():
    fuel_cells = [[0 for _ in range(300)] for _ in range(300)]
    for y in range(300):
        for x in range(300):
            fuel_cells[y][x] = power(x, y)

    max_fuel = -float('inf')
    max_fuel_loc = (-1, -1)
    for size in range(1, 301):
        for y in range(0, 301-size):
            for x in range(0, 301-size):
                s = 0
                for i in range(size):
                    for j in range(size):
                        s += fuel_cells[y+i][x+j]
                if s > max_fuel:
                    max_fuel = s
                    max_fuel_loc = (x+1, y+1, size)

    return max_fuel_loc

import numpy as np
from scipy.signal import convolve2d

def part_two_np():
    fuel_cells = np.array([[0 for _ in range(300)] for _ in range(300)])
    for y in range(300):
        for x in range(300):
            fuel_cells[y][x] = power(x, y)

    max_fuel = -float('inf')
    max_fuel_loc = (-1, -1)
    for size in range(1, 301):
        kernel = np.ones((size, size))
        ret = convolve2d(fuel_cells, kernel, mode='valid')
        y, x = np.unravel_index(ret.argmax(), ret.shape)
        val = ret[y, x]
        if val > max_fuel:
            max_fuel = val
            max_fuel_loc = (x+1, y+1, size)

    return max_fuel_loc

print(part_one())
print(part_two())
