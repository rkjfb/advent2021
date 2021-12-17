import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
grid = {}

x1 =x2=y1=y2=0

maxy = -9999

def parse():
    global grid

    data = open("data.txt", "r")
    rlines = data.readlines()

    line = rlines[0].strip()
    s = line.split(" ")
    sx = s[2][2:-1].split("..")
    sy = s[3][2:].split("..")

    global x1,x2,y1,y2
    x1 = int(sx[0])
    x2 = int(sx[1])
    y1 = int(sy[0])
    y2 = int(sy[1])

# fires at velocity return true if target is hit
def fire(dx, dy):
    cx = cy = 0

    loop_maxy = -9999

    while cx < x2 and cy >= y2:
        cx += dx
        cy += dy

        if dx > 0:
            dx -= 1

        dy -= 1

        if cy > loop_maxy:
            loop_maxy = cy

        if x1<=cx<=x2 and y1<=cy<=y2:
            global maxy
            if loop_maxy > maxy:
                maxy = loop_maxy
                print(dx,dy, "new maxy", maxy)
            return True

    return False


def main():
    parse()
    for x in range(10*abs(x2-x1)):
        for y in range(10*abs(y2-y1)):
            fire(x,y)
    #print(fire(7,2))
    #print(fire(6,3))
    #print(fire(9,0))
    #print(fire(17,-4))

main()


