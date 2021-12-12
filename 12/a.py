import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
nodes = {}
paths = 0
bonus = None
count = 0
current_path = []

class Node:
    def __init__(self, name):
        self.name = name
        self.next = []
        self.big = name.isupper()
        self.visited = 0

    def __repr__(self):
        return self.name

def recurse(rec):
    global current_path
    global bonus
    #print(len(current_path), "recurse", rec, current_path)
    if rec.name == "end":
        global paths
        #print("end", paths, current_path)
        paths += 1
        return

#    global count
#    count += 1
#    print("count", count)
#    if count > 5000:
#        return
#
#    if paths > 36:
#        raise "something is wrong"
#
#    if len(current_path) > 10:
#        raise "too deep"

    rec.visited += 1
    current_path.append(rec.name)
    clear_bonus = False
    for n in rec.next:
        global bonus
        visit = n.big or n.visited == 0
        if not visit and not n.big and n.name not in ["start", "end"] and bonus == None:
            #print("*** bonus recurse", n, len(current_path))
            visit = True
            bonus = n
            clear_bonus = True

        if visit:
            recurse(n)

        if clear_bonus:
            #print("*** clear bonus", bonus, len(current_path))
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


