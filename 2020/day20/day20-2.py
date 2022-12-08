#!/usr/bin/env python

from tile import Tile

print("\033[2J\033[H") # ]]

import pickle
with open('mega_tile.pickle', 'rb') as f:
    mega_tile = pickle.load(f)

nessy = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""[1:-1]
l = nessy.splitlines()

kernel = (len(l), len(l[0]))
poi = {
    (y, x) for x in range(kernel[1]) for y in range(kernel[0]) if l[y][x] == '#'
}
width, height = mega_tile.shape

for tile in mega_tile.permutations():
    is_nessy = set()
    for start_y in range(height-kernel[0]):
        for start_x in range(width-kernel[1]):
            nessy = {(y+start_y, x+start_x) for y, x in poi}
            if nessy.issubset(tile.points):
                is_nessy.update(nessy)
    if is_nessy:
        print(len(tile.points - is_nessy))
        exit()

print('JOBS_DONE')
