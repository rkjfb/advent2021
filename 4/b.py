import re
import json
import copy
#import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

draw = []
s = lines[0].split(",")
for e in s:
    draw.append(int(e))

print("lendraw", len(draw), "draw", draw)

boards = []
board = []

for i in range(1, len(lines)):
    line = lines[i]
    if line == "\n":
        continue

    s = line.split()
    row = []
    for e in s:
        row.append(int(e))

    if not len(row) == 5:
        print("bad row length")

    board.append(row)

    if len(board) == 5:
        boards.append(board)
        board = []

#print("boards", boards)
print("lenboards", len(boards))

# hits n on all boards
hits = set()
def hit(n):
    for i in range(len(boards)):
        for x in range(5):
            for y in range(5):
                if n == boards[i][x][y]:
                    if n == 64 and i == 63:
                        print("hitting 64 on board 63", boards[i][x][y])
                    hits.add((i,x,y))

completed_set = set()

def finished():

    for i in range(len(boards)):
        debug = False
        if i == 63 and len(hits) > 1100:
            print("interesting start")
            print("first record",  (63, 0, 0) in hits)
            debug = True

        if i in completed_set:
            continue

        found = False

        # search rows
        for x in range(5):
            c = 0
            for y in range(5):
                if (i,x,y) in hits:
                    c += 1
                    if c == 5:
                        found = True
                else:
                    if debug:
                        print("miss ", (i,x,y))
        if debug:
            print("row found=", found)

        # search columns
        for y in range(5):
            c = 0
            for x in range(5):
                if (i,x,y) in hits:
                    c += 1
                    if c == 5:
                        found = True

        if debug:
            print("column found=", found)
            if boards[i][0] == [64, 67, 11, 10, 92]:
                print("interesting board found=", found, "i", i, "lenhits", len(hits))

        # remember board and report sum of unmarked
        if found:
            completed_set.add(i)
            s = 0
            for x in range(5):
                for y in range(5):
                    if not (i,x,y) in hits:
                        s += boards[i][x][y]
            return s

    return 0

complete = 0
drawi = 0
while True:

    if drawi >= len(draw):
        print("debug dump")
        for i in range(len(boards)):
            for x in range(5):
                for y in range(5):
                    if not (i,x,y) in hits:
                        print("missing", (i,x,y))

        print("completed_set", completed_set)

        for i in range(len(boards)):
            if not i in completed_set:
                print("incomplete", boards[i])
                break

    hit(draw[drawi])
    #print("drawi", drawi, "draw", draw[drawi], "lenhits", len(hits))
    s = finished()
    if not s == 0:
        complete += 1
        #print("completed", s, "drawi", drawi, "draw", draw[drawi], "product", s * draw[drawi], "complete", complete)
        if not complete == len(completed_set):
            print("odd", complete, len(completed_set))

    if complete == len(boards):
        print("lastsum", s, "draw", draw[drawi], "product", s * draw[drawi])
        break

    drawi += 1


