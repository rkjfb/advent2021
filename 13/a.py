import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
grid = set()
split = []

def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    parse_folds = False

    for line in rlines:
        line = line.strip()
        if line == "":
            parse_folds = True
            continue

        if not parse_folds:
            print(line)
            x,y = line.split(",")
            grid.add((int(x), int(y)))
        else:
            s = line.split(" ")
            s2 = s[2].split("=")
            split.append((s2[0], int(s2[1])))

def fold(instr):
    global grid

    dim,pos = instr
    newgrid = set()
    for x,y in grid:
        if dim == "y":
            if y > pos:
                y = pos - (y - pos)
        if dim == "x":
            if x > pos:
                x = pos - (x - pos)

        newgrid.add((x,y))

    grid = newgrid

def draw():
    maxx = 0
    maxy = 0
    for x,y in grid:
        if x > maxx:
            maxx = x
        if y > maxy:
            maxy = y

    maxx += 1
    maxy += 1

    for y in range(maxy):
        row = ""
        for x in range(maxx):
            if (x,y) in grid:
                row += "#"
            else:
                row += "."
        print(row)

def main():
    parse()

    for f in split:
        fold(f)

    draw()

    print("dots", len(grid))

main()


