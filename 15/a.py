import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
grid = collections.defaultdict(int)
topleft = 9999
maxx = 0
maxy = 0

def parse():
    global template
    global rules

    data = open("data.txt", "r")
    rlines = data.readlines()

    y = 0
    for line in rlines:
        line = line.strip()

        x = 0
        for c in line:
            grid[(x,y)] = int(c)
            x += 1

        y += 1

    global maxx
    maxx = x-1
    global maxy
    maxy = y -1
    global topleft
    topleft = grid[(0,0)]

# does a djikstra'ish mark from bot right to top left of cumulative path
def mark():
    for x in range(maxx,-1,-1):
        for y in range(maxy,-1,-1):
            smaller = 0
            if x == maxx and y == maxy:
                smaller = 0
            elif x == maxx:
                smaller = grid[(x,y+1)]
            elif y == maxy:
                smaller = grid[(x+1,y)]
            else:
                smaller = min(grid[(x,y+1)], grid[(x+1,y)])

            grid[(x,y)] += smaller

def main():
    parse()
    mark()

    print("mincost", grid[(0,0)]-topleft)

main()


