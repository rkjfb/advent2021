import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
fish = []
newfish = []
canvas = collections.defaultdict(int)

class Fish:
    def __init__(self, t):
        self.t = t

    def tick(self):
        if self.t == 0:
            global newfish
            newfish.append(Fish(8))
            self.t = 6
        else:
            self.t -= 1

    def __repr__(self):
        return str(self.t)

def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    s = rlines[0].split(",")
    for e in s:
        i = int(e)
        fish.append(Fish(i))

def main():
    parse()

    for d in range(1, 80+1):
        for f in fish:
            f.tick()

        global newfish
        fish.extend(newfish)
        newfish = []

        #print("day ", d, " - ", fish)

    print("total fish", len(fish))

main()


