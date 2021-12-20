import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation

# useful problem state
decoder = ""
grid = None

# runs the decoding step at x,y
def decode(inx, iny):
    global grid
    key = ""
    for y in range(iny-1, iny+2):
        for x in range(inx-1, inx+2):
            key += str(grid[(x,y)])

    assert len(key) == 9

    intkey = int(key,2)
    ret = decoder[intkey]
    # print(key, intkey, ret)
    return ret

# runs 1 iteration of the algorithm
def iterate():
    global grid
    new_grid = None

    minx,miny,maxx,maxy = get_bounds()

    c = decode(maxx+10,maxy+10)
    if c == "#":
        print("iterate default 1", c)
        new_grid = collections.defaultdict(lambda:1)
    else:
        print("iterate default 0", c)
        new_grid = collections.defaultdict(lambda:0)

    print(minx,miny,maxx,maxy)

    for x in range(minx-1,maxx+2):
        for y in range(miny-1, maxy+2):
            c = decode(x,y)
            if c == "#":
                new_grid[(x,y)] = 1
            else:
                new_grid[(x,y)] = 0

#            print(x,y, "decode", c)

    grid = new_grid

# returns the number of 1s in grid
def count_pixels():
    return sum(grid.values())

# returns the x,y,x,y to iterate on
def get_bounds():
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    for e in grid.keys():
        x,y = e
        minx = min(x,minx)
        maxx = max(x,maxx)
        miny = min(y,miny)
        maxy = max(y,maxy)

    maxx += 1
    maxy += 1

    return minx,miny,maxx,maxy

# prints the grid
def print_grid():
    minx,miny,maxx,maxy = get_bounds()

    for y in range(miny,maxy):
        row = ""
        for x in range(minx,maxy):
            if grid[(x,y)] == 1:
                row += "#"
            else:
                row += "."
        print(row)
    print()

def parse():
    global decoder
    global grid

    data = open("data.txt", "r")
    rlines = data.readlines()

    decoder = rlines[0].strip()

    print("parse default 0")
    grid = collections.defaultdict(lambda:0)

    y = 0
    for line in rlines[2:]:
        line = line.strip()
        if line == "":
            continue

        x = 0
        for c in line:
            if c == "#":
                grid[(x,y)] = 1
            else:
                grid[(x,y)] = 0
            x += 1
        y += 1

def main():
    parse()
    print_grid()
    for i in range(50):
        iterate()

    print("count_pixels", count_pixels())

main()
