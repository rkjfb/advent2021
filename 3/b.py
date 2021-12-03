import re
import json
import copy
#import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

length = 0
infile = []

for line in lines:
    if line == "\n":
        continue

    if length == 0:
        length = len(line.strip())

    num = int(line, 2)
    infile.append(num)

# returns tuple <count ones>, <count zeros>
def count(l, mask):

    # count
    ones = 0
    zeros = 0

    for e in l:
        if e & mask != 0:
            ones += 1
        else:
            zeros += 1

    return ones, zeros

# filters l at mask on target
def filter(l, mask, target):
    out = []
    for e in l:
        if (e & mask == 0 and target == 0) or (e & mask != 0 and target == 1):
            out.append(e)

    return out

oxy = infile
for i in reversed(range(length)):
    mask = 1 << i
    ones, zeros = count(oxy, mask)

    target = 0
    if ones > zeros:
        target = 1
    if ones == zeros:
        target = 1

    oxy = filter(oxy, mask, target)

    if len(oxy) == 1:
        break


co = infile

for i in reversed(range(length)):
    mask = 1 << i
    ones, zeros = count(co, mask)

    target = 0
    if ones < zeros:
        target = 1
    if ones == zeros:
        target = 0 

    co = filter(co, mask, target)

    if len(co) == 1:
        break

print("oxy len", len(oxy))
print("oxy 0", bin(oxy[0]))

print("co len", len(co))
print("co 0", bin(co[0]))

print("product", oxy[0] * co[0])
