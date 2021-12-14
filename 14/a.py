import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
template = ""
rules = {}

def parse():
    global template
    global rules

    data = open("data.txt", "r")
    rlines = data.readlines()

    template = rlines[0].strip()

    for line in rlines[2:]:
        line = line.strip()

        s = line.split(" -> ")
        rules[s[0]] = s[1]


def step():
    global template
    global rules

    newt = ""
    last = ""

    for i in range(len(template)-1):
        m = template[i:i+2]

        n = m[0] + rules[m] 
        last = m[1]

        newt += n

    template = newt + last

def trange():
    count = collections.defaultdict(int)
    for c in template:
        count[c] += 1

    print("range", max(count.values()) - min(count.values()))

def main():
    parse()

    for i in range(10):
        step()

    trange()

main()


