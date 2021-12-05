import re
import json
import copy
#import numpy as np
from collections import deque
import math

# useful problem state
lines = []
canvas = []

class Line:
    def __init__(self,x1,y1,x2,y2):
        self.x1 = min(x1,x2)
        self.y1 = min(y1,y2)
        self.x2 = max(x1,x2)
        self.y2 = max(y1,y2) 

    def draw(self):
        if self.y1 == self.y2:
            for x in range(self.x1, self.x2+1):
                canvas[x][self.y1] += 1
        elif self.x1 == self.x2:
            for y in range(self.y1, self.y2+1):
                canvas[self.x1][y] += 1


def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    maxx = 0
    maxy = 0

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

        if x1 > maxx:
            maxx = x1
        if x2 > maxx:
            maxx = x2
        if y1 > maxy:
            maxy = y1
        if y2 > maxy:
            maxy = y2
    
    maxx += 1
    maxy += 1

    for x in range(maxx):
        col = []
        for y in range(maxy):
            col.append(0)
        canvas.append(col)

    print("canvas", maxx, maxy)

def main():
    parse()

    for l in lines:
        l.draw()

    #print(canvas)

    count = 0
    for c in canvas:
        for e in c:
            if e >= 2:
                count += 1

    print("count", count)

main()


