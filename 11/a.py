import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
floor = collections.defaultdict(lambda: 0)

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

    flashcount = 0

    for i in range(1,20+1):

        # round start, everyone gets incremented
        flash = []
        for y in range(maxy):
            for x in range(maxx):
                floor[(x,y)] += 1

                if floor[(x,y)] > 9:
                    flash.append((x,y))
        seen = set(flash)

        # chain flashes
        while len(flash) > 0:
            ix,iy = flash.pop()

            for x in range(-1, 2):
                for y in range(-1, 2):
                    floor[(ix+x,iy+y)] += 1
                    if floor[(ix+x,iy+y)] > 9 and not (ix+x, iy+y) in seen:
                        flash.append((ix+x,iy+y))
                        seen.add((ix+x, iy+y))

        flashcount += len(seen)

        # reset the flashes
        for y in range(maxy):
            for x in range(maxx):
                if floor[(x,y)] > 9:
                    floor[(x,y)] = 0

        # show what happened
        printfloor = True
        if printfloor:

            print("step", i)
            for y in range(maxy):
                r = ""
                for x in range(maxx):
                    r += str(floor[(x,y)])
                print(r)
            print()


    print("flashcount", flashcount)


def main():
    parse()

main()


