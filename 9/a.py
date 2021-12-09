import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
floor = collections.defaultdict(lambda: 10)

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

    risk = 0
    for y in range(maxy):
        for x in range(maxx):
            target = floor[(x,y)]
            if target < floor[(x-1,y)] and target < floor[(x+1,y)] and target < floor[(x,y-1)] and target < floor[(x,y+1)]:
                risk += target + 1

    print("risk", risk)

def main():
    parse()

main()


