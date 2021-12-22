import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation

# useful problem state
grid = collections.defaultdict(int)

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

def setgrid(on, x1,x2,y1,y2,z1,z2):
    for x in range(x1,x2+1):
        for y in range(y1, y2+1):
            for z in range(z1, z2+1):
                grid[(x,y,z)] = on

def parse():
    global decoder
    global grid

    data = open("data.txt", "r")
    rlines = data.readlines()

    for line in rlines:
        line = line.strip()
        if line == "":
            continue

        s = line.split(" ")
        on = 0
        if s[0] == "on":
            on = 1

        s = s[1].split(",")
        sx = s[0].split("..")
        x1 = max(int(sx[0][2:]), -50)
        x2 = min(int(sx[1]), 50)

        if x1 > 50 or x2 < -50:
            continue

        sy = s[1].split("..")
        y1 = max(int(sy[0][2:]), -50)
        y2 = min(int(sy[1]), 50)

        if y1 > 50 or y2 < -50:
            continue

        sz = s[2].split("..")
        z1 = max(int(sz[0][2:]), -50)
        z2 = min(int(sz[1]), 50)

        if z1 > 50 or z2 < -50:
            continue

        print(on, x1,x2,y1,y2,z1,z2)
        setgrid(on, x1,x2,y1,y2,z1,z2)


def main():
    parse()

    print("count_pixels", count_pixels())

main()
