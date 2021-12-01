import re
import json
import copy
#import numpy as np
from collections import deque
import math

data = open("data.txt", "r")
lines = data.readlines()

last = 999999999
increase = 0

for line in lines:
    if line == "\n":
        continue

    c = int(line)

    if c > last:
        increase += 1

    last = c

print("increase", increase)
