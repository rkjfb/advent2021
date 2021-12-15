import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
grid = collections.defaultdict(int)
distance = collections.defaultdict(lambda:99999999)
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
    global maxx
    global maxy
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
    maxx = (maxx+1)*5-1
    maxy = (maxy+1)*5-1


# does a djikstra'ish mark from bot right to top left of cumulative path
def mark():
    visited = set()
    distance[(maxx,maxy)] = grid[(maxx,maxy)]

    for x in range(maxx,-1,-1):
        for y in range(maxy,-1,-1):

            poslist = []

            if x+1 <= maxx:
                poslist.append((x+1,y))

            if x-1 >= 0:
                poslist.append((x-1,y))

            if y+1 <= maxy:
                poslist.append((x,y+1))

            if y-1 >= 0:
                poslist.append((x,y-1))

            for pos in poslist:
                if not pos in visited:
                    distance[pos] = min(distance[pos], distance[(x,y)] + grid[pos])

            visited.add((x,y))

def main():
    parse()
    #expand()
    mark()
    print(grid)
    print(distance)


    print("mincost", distance[(0,0)]-topleft)

main()


