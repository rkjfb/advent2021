import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
template = ""
rules = {}

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

def print_dict(d):
    dmax = max(d.values())
    cmax = max(d, key=d.get)
    dmin = min(d.values())
    cmin = min(d, key=d.get)

    print("range", cmax, dmax, cmin, dmin, dmax - dmin)


cache = []

# returns dict of characters at depth for 2 character string
def get(depth, cc):
    if cc in cache[depth]:
        return cache[depth][cc]

    if depth == 0:
        d = collections.defaultdict(int)
        for c in cc:
            d[c] += 1
    else:
        mid = rules[cc]
        lhs = get(depth-1, cc[0]+mid)
        rhs = get(depth-1, mid+cc[1])

        # create merged dict
        d = lhs.copy()
        for k,v in rhs.items():
            d[k] += v
        # double counted mid
        d[mid] -= 1

    cache[depth][cc] = d

    return d


def main():
    parse()

    for i in range(41):
        cache.append(dict())

    last = ""
    final_dict = collections.defaultdict(int)
    for i in range(len(template)-1):
        m = template[i:i+2]
        last = m[1]
        d = get(40, m)

        # merged 2 character dict in
        for k,v in d.items():
            final_dict[k] += v

        # don't double count the last character
        final_dict[last] -= 1

    # the last iteration last character should be restored
    final_dict[last] += 1

    print("final")
    print(final_dict)
    print_dict(final_dict)

main()


