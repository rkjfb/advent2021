import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation

# useful problem state
ground = collections.defaultdict(lambda:None)
maxx = 0
maxy = 0

def parse():
    global ground
    global maxx
    global maxy

    data = open("data.txt", "r")
    rlines = data.readlines()

    y = 0
    for line in rlines:
        line = line.strip()
        if line == "":
            continue

        x = 0
        for c in line:
            if c != ".":
                ground[(x,y)] = c
            x += 1

        y += 1

    maxx = x
    maxy = y

def print_ground():
    for y in range(maxy):
        row = ""
        for x in range(maxx):
            c = ground[(x,y)]
            if c != None:
                row += c
            else:
                row += "."
        print(row)

def main():
    parse()
    print_ground()

main()
