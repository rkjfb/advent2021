import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
known={
        0:"abcefg",
        1:"cf",
        2:"acdeg",
        3:"acdfg",
        4:"bcdf",
        5:"abdfg",
        6:"abdefg",
        7:"acf",
        8:"abcdefg",
        9:"abcdgf"
        }

# return unknown entry set of length
def get_known(i):
    s = set()
    for c in known[i]:
        s.add(c)
    return s

# return unknown entry set of length
def get_unknown(l, length):
    for e in l:
        if len(e) == length:
            s = set()
            for c in e:
                s.add(c)
            return s

    raise "fail"

# returns the union of all unknown segments of length
def get_unknown_multi(l, length):
    s = set()
    for e in l:
        if len(e) == length:
            for c in e:
                s.add(c)

    if len(s) == 0:
        raise "fail"

    return s

# return unknown entry set of length, if it contains match set
def get_unknown_set(l, length, match_set):
    for e in l:
        if len(e) == length:
            s = set()
            for c in e:
                s.add(c)

            if s.issuperset(match_set):
                return s

    raise "fail"


def solve(l):
    print("solve", l)

    # initially anything is possible
    can = {}
    for c in "abcedfg":
        can[c] = set()
        for i in "abcdefg":
            can[c].add(i)

    # filter candidates against known counts
    for i in [1,4,7,8]:
        k = known[i]
        u = get_unknown(l, len(k))
        for c in k:
            can[c] = can[c].intersection(u)

    print("known length filter\n", can)

    # insight: 7 has 1 extra segment on 1
    # subtract 1 candidates from 7
    unknown1 = get_unknown(l, len(known[1]))
    unknown7 = get_unknown(l, len(known[7]))
    unknownA = unknown7.difference(unknown1)
    can["a"] = set(unknownA)
    for c in "bcdefg":
        can[c] = can[c].difference(can["a"])

    print("7 contains 1 filter\n", can)

    # insight: 3 has len=5 and both of 1's segments
    unknown3 = get_unknown_set(l, len(known[3]), unknown1)
    for c in known[3]:
        can[c] = can[c].intersection(unknown3)

    print("3 has len=5 and contains 1\n", can)

    # filter: 2, 3 and 5 are length 5
    unknown235 = get_unknown_multi(l, 5)
    for c in known[2]:
        can[c] = can[c].intersection(unknown235)
    for c in known[3]:
        can[c] = can[c].intersection(unknown235)
    for c in known[5]:
        can[c] = can[c].intersection(unknown235)

    #print("len=5 235 club\n", can)

    # filter 2: 0,6,9 are length 6
    unknown069 = get_unknown_multi(l, 6)
    for c in known[0]:
        can[c] = can[c].intersection(unknown069)
    for c in known[6]:
        can[c] = can[c].intersection(unknown069)
    for c in known[9]:
        can[c] = can[c].intersection(unknown069)

    #print("len=6 069 club\n", can)

    # now make some guesses based on candidate segments
    for i in range(10):
        megaset = set()
        for c in known[i]:
            megaset = megaset.union(can[c])

        print("megaset", i, megaset)


def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    c = 0
    for line in rlines:
        s = line.split("|")
        l = s[0].strip().split(" ")
        solve(l)
        r = s[1].strip().split(" ")

        #for e in r:
        #    if len(e) in [2, 3, 4, 7]:
        #        c += 1

    #print("c", c)

def main():
    parse()

main()


