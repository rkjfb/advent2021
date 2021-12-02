import re
import json
import copy
#import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

depth = 0
forward = 0

for line in lines:
    if line == "\n":
        continue

    s = line.split(" ")

    cmd = s[0]
    delta = int(s[1])

    if cmd == "forward":
        forward += delta

    if cmd == "down":
        depth += delta

    if cmd == "up":
        depth -= delta 


print("depth", depth)
print("forward", forward)
print("product", forward*depth)
