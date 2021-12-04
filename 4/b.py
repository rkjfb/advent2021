import re
import json
import copy
#import numpy as np
from collections import deque
import math

draw = []
boards = []

def parse():

    data = open("data.txt", "r")
    lines = data.readlines()

    # draw list
    s = lines[0].split(",")
    for e in s:
        draw.append(int(e))

    print("lendraw", len(draw), "draw", draw)

    # board list
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


dump_everything = False

# hits n on all boards
hits = set()
def hit(n):
    for i in range(len(boards)):
        for x in range(5):
            for y in range(5):
                if n == boards[i][x][y]:
                    if n == 92 and i == 63:
                        print("hitting 92 on board 63", boards[i][x][y])
                        global dump_everything
                        dump_everything = True
                    hits.add((i,x,y))

complete = set()

def finished():

    if dump_everything:
        print("running finished, len boards", len(boards))

    for i in range(len(boards)):
        debug = False
        if i == 63 and dump_everything:
            print("on board 63: (63,0,0) in hits",  (63, 0, 0) in hits)
            debug = True

        if i in complete:
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
                    if debug and False:
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
            complete.add(i)
            s = 0
            for x in range(5):
                for y in range(5):
                    if not (i,x,y) in hits:
                        s += boards[i][x][y]
            if dump_everything:
                print("early out for board", i)
            return s

    return 0

def main():
    parse()

    drawi = 0
    while True:

        if drawi >= len(draw):
            print("debug dump")
            for i in range(len(boards)):
                for x in range(5):
                    for y in range(5):
                        if not (i,x,y) in hits:
                            print("missing", (i,x,y))

            print("complete", complete)

            for i in range(len(boards)):
                if not i in complete:
                    print("incomplete", boards[i])
                    break

        if dump_everything:
            print("drawi", drawi)
        hit(draw[drawi])

        s = 1

        while s != 0:
            # 1 draw might trigger >1 board
            s = finished()

            if len(complete) == len(boards):
                print("completed", s, "draw", draw[drawi], "product", s * draw[drawi])
                return

        drawi += 1

main()


