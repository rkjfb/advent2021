import re
import json
import copy
#import numpy as np
import collections
import math

class Node:
    def __init__(self):
        self.left = None
        self.right = None

    def __repr__(self):
        return "[" + str(self.left) + "," + str(self.right) + "]"

# useful problem state
root = None

# returns a Node, remaining s
def recurse_parse(s):
    if s[0] != "[":
        raise "bad parse"

    s = s[1:]

    n = Node()

    if s[0] in "0123456789":
        n.left = int(s[0])
        # 4,
        s = s[2:]
    elif s[0] == "[":
        n.left,s = recurse_parse(s)
        # ,
        s = s[1:]
    else:
        raise "unexpected char" 

    if s[0] in "0123456789":
        n.right = int(s[0])
        # 4]
        s = s[2:]
    elif s[0] == "[":
        n.right,s = recurse_parse(s)
        # ]
        s = s[1:]
    else:
        raise "unexpected char: "

    return n,s

def parse():
    global root

    data = open("data.txt", "r")
    rlines = data.readlines()

    for line in rlines:
        line = line.strip()

        root,s = recurse_parse(line)

        if s != "":
            raise "left overs"
        
        print("line", line, "root", root)



def main():
    parse()

main()


