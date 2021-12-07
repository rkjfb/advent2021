import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
crab = []
delta = []

def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    s = rlines[0].split(",")
    for e in s:
        i = int(e)
        crab.append(i)

    s = 0
    for i in range(10000):
        s += i
        delta.append(s)

    #print("delta", delta)
    #print("d11", delta[11])

def score(pos):
    s = 0
    for i in crab:
        s += delta[abs(pos-i)]

    return s

def main():
    parse()

    start = min(crab)
    end = max(crab)

    min_score = 99999999
    min_pos = 0

    for pos in range(start, end):
        s = score(pos)

        if s < min_score:
            min_score = s
            min_pos = pos

    print("score", min_score, "pos", min_pos)

main()


