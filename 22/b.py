import copy
import collections
import math

# return True if o contains i
def contains(o, i):
    (ox1,ox2,oy1,oy2,oz1,oz2) = o
    (ix1,ix2,iy1,iy2,iz1,iz2) = i

    if ox1 <= ix1 and ix2 <= ox2:
        if oy1 <= iy1 and iy2 <= oy2:
            if oz1 <= iz1 and iz2 <= oz2:
                return True
    return False

# return True if o and i intersect
def intersects_(o, i):
    (ox1,ox2,oy1,oy2,oz1,oz2) = o
    (ix1,ix2,iy1,iy2,iz1,iz2) = i

    if ix2 <= ox1 or ix1 >= ox2:
        return False
    if iy2 <= oy1 or iy1 >= oy2:
        return False
    if iz2 <= oz1 or iz1 >= oz2:
        return False

    return True


# returns the number of 1s in grid
def old_count_pixels():
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

# list of steps from input
steps = []
reversed_steps = None

# sorted x,y,z segments
x_segments = []
y_segments = []
z_segments = []

# build a sorted segment list from a set of offsets
def build_segment(s):
    seg = []
    l = sorted(s)

    start = l[0]
    for n in l[1:]:
        seg.append((start,(n-start)))
        # todo: segment-specific step list
        start = n

    return seg

def build_all_segments():
    global x_segments
    global y_segments
    global z_segments

    x_set = set()
    y_set = set()
    z_set = set()

    for s in steps:
        (on,x1,x2,y1,y2,z1,z2) = s
        x_set.add(x1)
        x_set.add(x2)
        y_set.add(y1)
        y_set.add(y2)
        z_set.add(z1)
        z_set.add(z2)

    x_segments = build_segment(x_set)
    y_segments = build_segment(y_set)
    z_segments = build_segment(z_set)

# 1d x-axis result of running steps
def step_x(y,z):
    count_pixels = 0
    for (start,seg_range) in x_segments:
        pixels_on = 0
        for s in reversed_steps:
            #print("step_x", s)
            (on,x1,x2,y1,y2,z1,z2) = s
            if y<y1 or y >=y2:
                continue
            if z<z1 or z >=z2:
                continue
            if x1<=start<x2:
                pixels_on = on
                # last segment writer wins
                break

        if pixels_on == 1:
            count_pixels += seg_range

    return count_pixels

def step_y(z):
    count_pixels = 0
    for (start,seg_range) in y_segments:
        row_pixels = 0
        for s in reversed_steps:
            (on,x1,x2,y1,y2,z1,z2) = s
            if z<z1 or z >=z2:
                continue
            if y1<=start<y2:
                row_pixels = step_x(start, z)
                # last segment writer wins
                break

        count_pixels += seg_range*row_pixels

    return count_pixels

def count_pixels():
    total = 0
    for (start,seg_range) in z_segments:
        print("z_segment", start, seg_range)
        plane_pixels = 0
        for s in reversed_steps:
            (on,x1,x2,y1,y2,z1,z2) = s
            if z1<=start<z2:
                plane_pixels = step_y(start)
                # last segment writer wins
                break

        total += seg_range*plane_pixels

    return total

def parse():
    global steps
    global reversed_steps

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

        steps.append((on,x1,x2,y1,y2,z1,z2))

    reversed_steps = steps.copy()
    reversed_steps.reverse()

def main():
    parse()
    build_all_segments()
    print("count_pixels", count_pixels())

main()
