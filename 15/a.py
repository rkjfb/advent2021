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

# expands grid by 5x5
def expand():
    global grid
    newgrid = collections.defaultdict(int)
    width = maxx+1
    height = maxy+1

    for ox in range(5):
        for oy in range(5):
            for x in range(maxx+1):
                for y in range(maxy+1):
                    value = grid[(x,y)]
                    delta = ox+oy
                    newvalue = value+delta
                    if newvalue > 9:
                        newvalue -= 9
                    newx = ox * width + x
                    newy = oy * height + y
                    newgrid[(newx,newy)] = newvalue

    grid = newgrid


# does a djikstra'ish mark from bot right to top left of cumulative path
def mark():
    megamaxx = (maxx+1)*5-1
    megamaxy = (maxy+1)*5-1
    for x in range(megamaxx,-1,-1):
        for y in range(megamaxy,-1,-1):
            smaller = 0
            if x == megamaxx and y == megamaxy:
                smaller = 0
            elif x == megamaxx:
                smaller = grid[(x,y+1)]
            elif y == megamaxy:
                smaller = grid[(x+1,y)]
            else:
                smaller = min(grid[(x,y+1)], grid[(x+1,y)])

            grid[(x,y)] += smaller

def main():
    parse()
    expand()
    #print(grid)
    mark()

    print("mincost", grid[(0,0)]-topleft)

main()


