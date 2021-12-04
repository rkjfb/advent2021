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

print("draw", draw)

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

    board.append(row)

    if len(board) == 5:
        boards.append(board)
        board = []

#print("boards", boards)

# hits n on all boards
hits = set()
def hit(n):
    for i in range(len(boards)):
        for x in range(5):
            for y in range(5):
                if n == boards[i][x][y]:
                    hits.add((i,x,y))

def finished():

    for i in range(len(boards)):
        found = False

        # search rows
        for x in range(5):
            c = 0
            for y in range(5):
                if (i,x,y) in hits:
                    c += 1
                    if c == 5:
                        found = True

        # search columns
        for y in range(5):
            c = 0
            for x in range(5):
                if (i,x,y) in hits:
                    c += 1
                    if c == 5:
                        found = True

        if found:
            s = 0
            for x in range(5):
                for y in range(5):
                    if not (i,x,y) in hits:
                        s += boards[i][x][y]
            return s

    return 0

drawi = 0
while True:
    hit(draw[drawi])
    s = finished()
    if not s == 0:
        print("sum", s, "draw", draw[drawi], "product", s * draw[drawi])
        break

    drawi += 1


