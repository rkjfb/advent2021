import re
import json
import copy
#import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

length = 0
zeros = []
ones = []

for line in lines:
    if line == "\n":
        continue

    if length == 0:
        length = len(line.strip())
        for i in range(length):
            ones.append(0)
            zeros.append(0)


    num = int(line, 2)

    for i in range(length):
        if num & 1 == 1:
            ones[i] += 1
        else:
            zeros[i] += 1

        num = num >> 1

gamma = 0
epsilon = 0

for i in reversed(range(length)):
    if ones[i] > zeros[i]:
        gamma = gamma | 1
    else:
        epsilon = epsilon | 1

    gamma = gamma << 1
    epsilon = epsilon << 1

gamma = gamma >> 1
epsilon = epsilon >> 1

print("ones", ones)
print("zeros", zeros)
print("length", length)
print("gamma", bin(gamma))
print("epsilon", bin(epsilon))
print("product", gamma*epsilon)
