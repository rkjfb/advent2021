import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation

class Node:
    def __init__(self, x,y,z, size, depth):
        # center of cube
        self.x = x
        self.y = y
        self.z = z
        # cube bounds (center-size/2)x(center+size/2)
        assert math.log2(size).is_integer(), "need to use power of 2 size"
        assert size >= 1, "should have at least size 1"
        self.size = size
        # cube is entirely full
        self.full = False
        # 8 children or None
        self.children = None
        self.depth = depth

    def max(self):
        halfsize = self.size //2
        return (self.x-halfsize, 
                self.x+halfsize, 
                self.y-halfsize, 
                self.y+halfsize, 
                self.z-halfsize, 
                self.z+halfsize)

    # return True if o contains i
    def contains(self, o, i):
        (ox1,ox2,oy1,oy2,oz1,oz2) = o
        (ix1,ix2,iy1,iy2,iz1,iz2) = i

        if ox1 <= ix1 and ix2 <= ox2:
            if oy1 <= iy1 and iy2 <= oy2:
                if oz1 <= iz1 and iz2 <= oz2:
                    return True
        return False

    # return True if o and i intersect
    def intersects_(self, o, i):
        (ox1,ox2,oy1,oy2,oz1,oz2) = o
        (ix1,ix2,iy1,iy2,iz1,iz2) = i

        if ix2 <= ox1 or ix1 >= ox2:
            return False
        if iy2 <= oy1 or iy1 >= oy2:
            return False
        if iz2 <= oz1 or iz1 >= oz2:
            return False

        return True

    # ensure that we have children
    def ensure_children_(self):
        if not self.children == None:
            return

        self.children = []
        halfsize = self.size//2
        assert halfsize >= 1
        quartersize = halfsize/2
        assert quartersize >= 0.5
        # print("instantiate children", halfsize, quartersize)
        for x in [self.x-quartersize, self.x+quartersize]:
            for y in [self.y-quartersize, self.y+quartersize]:
                for z in [self.z-quartersize, self.z+quartersize]:
                    self.children.append(Node(x,y,z,halfsize,self.depth+1))

    def add(self, p):
        if not self.intersects_(p, self.max()):
            #print(self.max(), "add", p, " - no intersection")
            return

        if self.contains(p, self.max()):
            #print(self.max(), "add", p, " - full containment")
            self.full = True
            self.children = None
            return

        #print(self.max(), "add", p)

        # partial containment
        self.ensure_children_()

        for c in self.children:
            c.add(p)

    def subtract(self, p):
        if not self.intersects_(p, self.max()):
            #print(self.max(), "subtract", p, " - no intersection")
            return

        if self.contains(p, self.max()):
            print(self.max(), "subtract", p, " - full containment")
            self.full = False
            self.children = None
            return

        print(self.max(), "subtract", p)

        # partial intersection, allocate full children so we can intersect
        self.ensure_children_()

        if self.full:
            self.full = False
            for c in self.children:
                c.full = True

        for c in self.children:
            c.subtract(p)

    def sum(self):
        if self.full:
            return self.size * self.size * self.size

        if self.children == None:
            return 0

        total = 0
        for c in self.children:
            total += c.sum()

        return total

    def __repr__(self):
        ret = str(self.depth) + ", " + str(self.size) + ": " 
        if self.full:
            return ret + "full"
        return ret + str(self.children) 

    def print_tree(self,depth):
        print(depth, self)
        if self.children != None:
            for c in self.children:
                c.print_tree(depth+1)

def parse():
    global decoder
    global grid

    data = open("data.txt", "r")
    rlines = data.readlines()

    root = Node(0,0,0,128, 0)

    for line in rlines:
        line = line.strip()
        if line == "":
            continue

        s = line.split(" ")
        on = 0
        if s[0] == "on":
            on = 1

        s = s[1].split(",")
        sx = s[0].split("..")
        x1 = max(int(sx[0][2:]), -50)
        x2 = min(int(sx[1])+1, 50)

        if x1 > 50 or x2 < -50:
            continue

        sy = s[1].split("..")
        y1 = max(int(sy[0][2:]), -50)
        y2 = min(int(sy[1])+1, 50)

        if y1 > 50 or y2 < -50:
            continue

        sz = s[2].split("..")
        z1 = max(int(sz[0][2:]), -50)
        z2 = min(int(sz[1])+1, 50)

        if z1 > 50 or z2 < -50:
            continue

        p = (x1,x2,y1,y2,z1,z2)
        print(on, p)
        assert root.contains(root.max(), p)
        if on == 1:
            root.add(p)
        else:
            #print("skip subtract")
            root.subtract(p)

    print("sum", root.sum())
    #print(root)
    #root.print_tree(0)

def main():
    parse()

main()
