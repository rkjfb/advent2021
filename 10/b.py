import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
floor = collections.defaultdict(lambda: 9)

# returns the recursive basin size at (x,y)
# destructively: replacing visited cells with 9
def recurse(x,y):
    print("recurse", x, y)
    c = 1
    floor[(x,y)] = 9

    points = [ (x-1,y), (x+1,y), (x,y-1), (x,y+1)]
    for p in points:
        if floor[p] != 9:
            c += recurse(*p)

    return c

def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    y = 0
    for line in rlines:
        line = line.strip()
        x = 0
        for c in line:
            floor[(x,y)] = int(c)
            x += 1
        y += 1

    maxx = x 
    maxy = y 

    basin = []
    #for y in range(maxy):
    #    for x in range(maxx):
    for y in range(maxy):
        for x in range(maxx):
            target = floor[(x,y)]
            if target != 9:
                size = recurse(x,y)
                basin.append(size)

    basin.sort(reverse=True)

    print("basin", basin)

    print("basinprod", basin[0] * basin[1] * basin[2])


def main():
    parse()

main()


