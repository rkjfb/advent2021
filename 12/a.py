import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
nodes = {}
paths = 0
# node we're currently giving a bonus visit to, if any
bonus = None
current_path = []

class Node:
    def __init__(self, name):
        self.name = name
        self.next = []
        self.big = name.isupper()
        # needs to be a count for bonus unwind case (2->1, still counts as visited for non-bonus purposes)
        self.visited = 0

    def __repr__(self):
        return self.name

def recurse(rec):
    global current_path
    global bonus
    if rec.name == "end":
        global paths
        paths += 1
        return

    rec.visited += 1
    current_path.append(rec.name)
    for n in rec.next:
        clear_bonus = False
        visit = n.big or n.visited == 0
        if not visit and not n.big and n.name not in ["start", "end"] and bonus == None:
            visit = True
            bonus = n
            clear_bonus = True

        if visit:
            recurse(n)

        if clear_bonus:
            bonus = None

    rec.visited -= 1
    current_path.pop(-1)


def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    for line in rlines:
        line = line.strip()
        a,b = line.split("-")
        if not a in nodes:
            nodes[a] = Node(a)
        if not b in nodes:
            nodes[b] = Node(b)

        an = nodes[a]
        bn = nodes[b]

        an.next.append(bn)
        bn.next.append(an)

def main():
    parse()

    recurse(nodes["start"])

    print("paths", paths)

main()


