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

    c = 0
    for line in rlines:
        s = line.split("|")
        r = s[1].strip().split(" ")
        for e in r:
            if len(e) in [2, 3, 4, 7]:
                print("--" + e + "--")
                c += 1

    print("c", c)

def main():
    parse()

main()


