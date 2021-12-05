import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
lines = []
canvas = collections.defaultdict(int)

class Line:
    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2 
        self.length = max(abs(x1-x2),abs(y1-y2)) + 1

    def draw(self):
        dx = 0
        dy = 0

        if self.x1 < self.x2:
            dx = 1
        if self.x1 > self.x2:
            dx = -1
        if self.y1 < self.y2:
            dy = 1
        if self.y1 > self.y2:
            dy = -1

        cx = self.x1
        cy = self.y1
        for i in range(self.length):
            canvas[(cx,cy)] += 1
            cx += dx
            cy += dy

    def __repr__(self):
        return str(self.x1) +", " + str(self.y1) + " -> " + str(self.x2) + ", " + str(self.y2)

def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    for line in rlines:
        s = line.split(" -> ")
        s1 = s[0].split(",")
        x1 = int(s1[0])
        y1 = int(s1[1])

        s2 = s[1].split(",")
        x2 = int(s2[0])
        y2 = int(s2[1])

        l = Line(x1,y1,x2,y2)

        lines.append(l)

def main():
    parse()

    for l in lines:
        l.draw()

    count = 0
    for k,v in canvas.items():
        if v >= 2:
            count += 1

    print("count", count)

main()


