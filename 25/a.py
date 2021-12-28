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
    global ground
    for y in range(maxy):
        row = ""
        for x in range(maxx):
            c = ground[(x,y)]
            if c != None:
                row += c
            else:
                row += "."
        print(row)
    print()

def step_east():
    global ground
    new_ground = collections.defaultdict(lambda:None)
    for k,v in ground.items():
        (x,y) = k
        if v == ">":
            nx = (x + 1) % maxx
            if (nx,y) not in ground or ground[(nx,y)] == None:
                new_ground[(nx,y)] = v
            else:
                new_ground[(x,y)] = v
        elif v == "v":
            new_ground[(x,y)] = v
        else:
            assert v == None

    ground = new_ground

def step_south():
    global ground
    new_ground = collections.defaultdict(lambda:None)
    for k,v in ground.items():
        (x,y) = k
        if v == "v":
            ny = (y + 1) % maxy
            if (x,ny) not in ground or ground[(x,ny)] == None:
                new_ground[(x,ny)] = v
            else:
                new_ground[(x,y)] = v
        elif v == ">":
            new_ground[(x,y)] = v
        else:
            assert v == None

    ground = new_ground

# returns True if a change occured
def step():
    global ground
    initial_ground = ground

    step_east()
    step_south()

    change = False
    for k,v in initial_ground.items():
        if v != None and v in ">v":
            if ground[k] != v:
                change = True
                break

    return change

def main():
    parse()
    print_ground()
    for i in range(1000):
        change = step()
        if not change:
            print("step", i+1, change)
            print_ground()
            break

main()
