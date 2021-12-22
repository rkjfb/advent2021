import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation

# useful problem state

# 100x100x100 completely full/empty cells, indexed by lowest value corner
# eg. key (0,0,0) goes all the way to (100,100,100)
# it includes (0,0,0) and excludes (100,100,100)
res = 100
high_grid = collections.defaultdict(int)

# dict of 1x1x1 cells for high_grid edges
low_grid = dict()

# returns the number of 1s in grid
def count_pixels():
    return sum(grid.values())

# returns the high_range of (lo,hi)
# note that n2 might be less than n1
def high_range(x1, x2):
    n1 = x1 - (x1 % res) + res
    n2 = x2 - (x2 % res)
    return (n1,n2)


def setgrid(on, x1,x2,y1,y2,z1,z2):
    # set the high bits
    (hix1,hix2) = high_range(x1,x2)
    (hiy1,hiy2) = high_range(y1,y2)
    (hiz1,hiz2) = high_range(z1,z2)
    for x in range(hix1,hix2,100):
        for y in range(hiy1,hiy2,100):
            for z in range(hiz1,hiz2,100):
                high_range[(x,y,x)] = 1


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
