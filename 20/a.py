import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation

# useful problem state
decoder = ""
grid = collections.defaultdict(int)

# returns the x,y,x,y to iterate on
def get_bounds():
    minx = 99999
    maxx = -99999
    miny = 99999
    maxy = -99999
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

def parse():
    global decoder

    data = open("data.txt", "r")
    rlines = data.readlines()

    decoder = rlines[0].strip()

    y = 0
    for line in rlines[2:]:
        line = line.strip()
        if line == "":
            continue

        x = 0
        for c in line:
            if c == "#":
                grid[(x,y)] = 1
            x += 1
        y += 1

def main():
    parse()
    print_grid()

main()
