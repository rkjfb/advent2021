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


# returns array[digit]=set(unknown segments)
def solve(l):
    # array of sets of unknown segments
    unknown = []
    for i in range(10):
        unknown.append(set())

    # unique length sets
    for i in [1,4,7,8]:
        unknown[i] = get_unknown(l, len(known[i]))

    # length 6 club: 0, 6, 9
    for e in l:
        if len(e)==6:
            s = set()
            for c in e:
                s.add(c)

            if s.issuperset(unknown[1]):
                if s.issuperset(unknown[4]):
                    # 9
                    unknown[9] = s
                else:
                    unknown[0] = s
            else:
                unknown[6] = s

    # length 5 club: 2,3,5
    # insight: 3 has len=5 and both of 1's segments
    unknown[3] = get_unknown_set(l, len(known[3]), unknown[1])
    for e in l:
        if len(e)==5:
            s = set()
            for c in e:
                s.add(c)

            if s != unknown[3]:
                if unknown[6].issuperset(s):
                    unknown[5] = s
                else:
                    unknown[2] = s

    return unknown

# give unknown from solve, and segments string
# returns int
def lookup(unknown, segments):
    s = set()
    for c in segments:
        s.add(c)

    for i in range(10):
        if s == unknown[i]:
            return i

    raise "fail"

def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    c = 0
    for line in rlines:
        s = line.split("|")
        l = s[0].strip().split(" ")
        unknown = solve(l)
        r = s[1].strip().split(" ")

        rhs = 0

        for e in r:
            rhs = rhs * 10 + lookup(unknown, e)

        c += rhs

    print("c", c)

def main():
    parse()

main()


