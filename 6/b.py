import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
fish = [0,0,0,0, 0,0,0,0, 0]

def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    s = rlines[0].split(",")
    for e in s:
        i = int(e)
        fish[i] += 1

def main():
    parse()

    new = 0

    for d in range(1, 256+1):
        global fish

        new = fish.pop(0)

        fish[6] += new
        fish.append(new)

        #print("day ", d, " - ", fish)

    print("total fish", sum(fish))

main()


