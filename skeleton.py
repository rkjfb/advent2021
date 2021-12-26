import re
import json
import copy
#import numpy as np
from collections import deque
import math

# useful problem state
draw = []
boards = []

def parse():
    data = open("data.txt", "r")
    lines = data.readlines()

    s = lines[0].split(",")
    for e in s:
        draw.append(int(e))

def main():
    parse()

    print("solution", 42)

main()


