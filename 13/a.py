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

def main():
    parse()

    fold(split[0])

    print("dots", len(grid))

main()


