#!/usr/bin/env python

from aocd import get_data


data = get_data(year=2022, day=2, block=True)
lines = data.splitlines()

ROCKA = "A"
PAPERA = "B"
SCIA = "C"

ROCKB = LOSE = "X"
PAPERB = TIE = "Y"
SCIB = WIN = "Z"

score = {
    ROCKA: {
        ROCKB: 4,
        PAPERB: 8,
        SCIB: 3,
    },
    PAPERA: {
        ROCKB: 1,
        PAPERB: 5,
        SCIB: 9,
    },
    SCIA: {
        ROCKB: 7,
        PAPERB: 2,
        SCIB: 6,
    }
}

choice = {
    ROCKA: {
        LOSE: SCIB,
        WIN: PAPERB,
        TIE: ROCKB,
    },
    PAPERA: {
        LOSE: ROCKB,
        WIN: SCIB,
        TIE: PAPERB,
    },
    SCIA: {
        LOSE: PAPERB,
        WIN: ROCKB,
        TIE: SCIB,
    }
}

# Part A

total = 0
for line in lines:
    a, b = line.split()
    total += score[a][b]

print(total)

# Part B

total = 0
for line in lines:
    a, b = line.split()
    c = choice[a][b]
    total += score[a][c]
    
print(total)
