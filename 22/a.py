import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation

# total number of nodes allocated
node_count = 0
grid_node_count = 0


class Node:
    def __init__(self, x,y,z, size, depth):
        global node_count
        node_count += 1
        if node_count % 1000 == 0:
            print("node_count", node_count, "grid_node_count", grid_node_count)
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
        assert halfsize >= grid_transition
        quartersize = halfsize//2
        assert quartersize >= 1

        # print("instantiate children", halfsize, quartersize)
        for x in [self.x-quartersize, self.x+quartersize]:
            for y in [self.y-quartersize, self.y+quartersize]:
                for z in [self.z-quartersize, self.z+quartersize]:
                    if halfsize == grid_transition:
                        self.children.append(GridNode(x,y,z,halfsize,self.depth+1))
                    else:
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
            #print(self.max(), "subtract", p, " - full containment")
            self.full = False
            self.children = None
            return

        #print(self.max(), "subtract", p)

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
            ret = self.size * self.size * self.size
            #print("fullret", ret)
            return ret

        if self.children == None:
            return 0

        total = 0
        for c in self.children:
            total += c.sum()

        #print("totalret", total)
        return total

    def __repr__(self):
        ret = str(self.depth) + ", " + str(self.size) + ": " 
        if self.full:
            return ret + "full"
        if self.children != None:
            ret = "\n" + ret
        return ret + str(self.children) 

    def print_tree(self,depth):
        print(depth, self)
        if self.children != None:
            for c in self.children:
                c.print_tree(depth+1)

# node, but using a dict
class GridNode(Node):
    def __init__(self, x,y,z, size, depth):
        super(GridNode, self).__init__(x,y,z,size,depth)
        global grid_node_count
        grid_node_count += 1
        self.grid = collections.defaultdict(int)

    def setgrid_(self, on, x1,x2,y1,y2,z1,z2):
        (mx1,mx2,my1,my2,mz1,mz2) = self.max()
        for x in range(max(x1,mx1),min(x2,mx2)):
            for y in range(max(y1,my1),min(y2,my2)):
                for z in range(max(z1,mz1),min(z2,mz2)):
                    self.grid[(x,y,z)] = on

    def add(self, p):
        self.setgrid_(1, *p)

    def subtract(self, p):
        self.setgrid_(0, *p)

    def sum(self):
        return sum(self.grid.values())

    def __repr__(self):
        ret = str(self.depth) + ", grid: " + str(self.sum())
        return ret

# when we transition from node to grid
max_size = 2 ** 20
root = Node(0,0,0,max_size, 0)
grid_transition = min(32, max_size//2)

# part 1 state, used for verification
ggrid = collections.defaultdict(int)

# returns the number of 1s in grid
def count_pixels():
    return sum(ggrid.values())

def setgrid(on, x1,x2,y1,y2,z1,z2):
    for x in range(x1,x2):
        for y in range(y1, y2):
            for z in range(z1, z2):
                ggrid[(x,y,z)] = on

# return (True, limitedx1, limitedx2) for continuation
def range_limit(x1, x2):
    part2 = True

    if part2:
        return (True, x1, x2)

    nx1 = max(x1, -50)
    nx2 = min(x2, 50)

    if nx1 > 50 or nx2 < -50:
        return (False,0,0)

    return (True, nx1, nx2)

def parse():
    global decoder
    global ggrid
    global root

    data = open("data.txt", "r")
    rlines = data.readlines()


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
        (c,x1,x2) = range_limit(int(sx[0][2:]), int(sx[1])+1)
        if not c:
            continue

        sy = s[1].split("..")
        (c,y1,y2) = range_limit(int(sy[0][2:]), int(sy[1])+1)
        if not c:
            continue

        sz = s[2].split("..")
        (c,z1,z2) = range_limit(int(sz[0][2:]), int(sz[1])+1)
        if not c:
            continue

        p = (x1,x2,y1,y2,z1,z2)
        print(on, p)
        assert root.contains(root.max(), p)
        if on == 1:
            root.add(p)
        else:
            #print("skip subtract")
            root.subtract(p)

        check = False
        if check:
            setgrid(on, x1,x2,y1,y2,z1,z2)
            newc = root.sum()
            oldc = count_pixels()

            if newc != oldc:
                print("failed", oldc, newc)
                assert False

    print("sum", root.sum())
    print("node_count", node_count, "grid_node_count", grid_node_count)
    #print(root)
    #root.print_tree(0)

def main():
    parse()

main()
