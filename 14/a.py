import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
template = ""
rules = {}

# cache of CC->10 step expansion template->string
cache_exp = {}

#cache of CC->10 step expansion->count dict
cache_dict= {}

def parse():
    global template
    global rules

    data = open("data.txt", "r")
    rlines = data.readlines()

    template = rlines[0].strip()

    for line in rlines[2:]:
        line = line.strip()

        s = line.split(" -> ")
        rules[s[0]] = s[1]


# returns expansion of t
def step(t):
    newt = ""
    last = ""

    for i in range(len(t)-1):
        m = t[i:i+2]

        n = m[0] + rules[m] 
        last = m[1]

        newt += n

    return newt + last

# populates cache for cc
def gen(cc):
    print("gen", cc)

    t = cc
    for i in range(1):
        t = step(t)

    cache_exp[cc] = t

    count = collections.defaultdict(int)
    for c in t:
        count[c] += 1

    global cache_dict
    cache_dict[cc] = count

def print_dict(d):
    dmax = max(d.values())
    cmax = max(d, key=d.get)
    dmin = min(d.values())
    cmin = min(d, key=d.get)

    print("range", cmax, dmax, cmin, dmin, dmax - dmin)

# returns the count dict of t expanded to depth
def recurse(t, depth):
    #print("start", depth, t)
    last = ""

    ret_dict = collections.defaultdict(int)

    for i in range(len(t)-1):
        m = t[i:i+2]
        last = m[1]

        if not m in cache_exp:
            gen(m)

        n = cache_exp[m] 

        if depth == 1:
            d = cache_dict[m]
            d[last] -= 1
            #print("depth1", n)
            #print_dict(d)
            #print(d)
        else:
            d = recurse(n, depth - 1)

        for k,v in d.items():
            ret_dict[k] += v

    #ret_dict[last] += 1

    #print("end", depth, t)
    #print_dict(ret_dict)
    #print(ret_dict)
    return ret_dict

def main():
    parse()

    d = recurse(template, 10)
    d[template[-1]] += 1
    print("final")
    print_dict(d)


main()


