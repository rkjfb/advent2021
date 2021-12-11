import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
floor = []

def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    for line in rlines:
        line = line.strip()
        row = []
        for c in line:
            row.append(int(c))
        floor.append(row)

    # technically flipped
    maxx = len(floor)
    maxy = len(floor[0])

    flashcount = 0

    i = 1
    #while True:
    for i in range(2):

        # round start, everyone gets incremented
        flash = []
        for y in range(maxy):
            for x in range(maxx):
                floor[x][y] += 1

                if floor[x][y] > 9:
                    flash.append((x,y))
        seen = set(flash)

        # chain flashes
        while len(flash) > 0:
            ix,iy = flash.pop()

            for x in range(-1, 2):
                for y in range(-1, 2):
                    xx = ix+x
                    yy = iy+y
                    if 0 <= xx < maxx and 0 <= yy < maxy:
                        floor[xx][yy] += 1
                        if floor[xx][yy] > 9 and not (xx,yy) in seen:
                            flash.append((xx,yy))
                            seen.add((xx, yy))

        flashcount += len(seen)

        # reset the flashes
        for y in range(maxy):
            for x in range(maxx):
                if floor[x][y] > 9:
                    floor[x][y] = 0

        # show what happened
        printfloor = True 
        if printfloor:

            print("step", i)
            for y in range(maxy):
                r = ""
                for x in range(maxx):
                    r += str(floor[x][y])
                print(r)
            print()

        if sum(sum(floor, []))==0:
            print("zeros at step", i)
            break
        
        i += 1


    print("flashcount", flashcount)


def main():
    parse()

main()


