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
all_set = set(["a", "b", "c", "d", "e", "f","g"])

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

        # for each segment in a known number we know it must be composed of unknown segments from the same length
        # eg. 1 is the only length 2, uses known segments "cf", therefore each of those segments can only possibly
        #     be whatever the current 2 segment unknown is.
        for c in k:
            can[c] = can[c].intersection(u)

        # the inverse is also true
        # eg. segments not in 1 (ie. all-'cf') can only possibly be whatever was in the not-1 segments
        k_set = get_known(i)
        k_inverse = all_set.difference(k_set)
        u_inverse = all_set.difference(u)
        for c in k_inverse:
            can[c] = can[c].intersection(u_inverse)

    # now make some guesses based on candidate segments
    candidate_numbers = set()
    for i in range(10):
        candidate_numbers.add(i)

    while len(candidate_numbers) > 0:
        match = -1

        for i in candidate_numbers:
            # the set of all segments that could possibly contribute to i
            megaset = set()
            for c in known[i]:
                megaset = megaset.union(can[c])

            count = 0
            for j in l:
                j_set = set()
                for j_c in j:
                    j_set.add(j_c)
                if megaset == j_set:
                    count += 1

            if count == 1:
                match = i
                print("match ", i, megaset)
                break

        if match != -1:
            candidate_numbers.remove(match)


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


