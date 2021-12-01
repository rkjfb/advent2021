import re
import json
import copy
#import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()


# a is a list of sliding window sums
a = []
win = deque()

for line in lines:
    if line == "\n":
        continue

    c = int(line)

    win.append(c)

    if len(win) > 3:
        win.popleft()

    if len(win) == 3:
        a.append(sum(win))

last = 999999999
increase = 0

for c in a:

    if c > last:
        increase += 1

    last = c

print("increase", increase)
