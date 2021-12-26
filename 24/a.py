import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation

# useful problem state
program_input = "1323"
program_input_index = 0
reg = { "w" : 0, "x" : 0, "y" : 0, "z" : 0 }

def parse_right(s):
    if len(s) < 3:
        return None

    r = s[2]

    if r[0].isalpha():
        return reg[r]

    return int(r)

def inp(r):
    global program_input
    global program_input_index
    global reg

    reg[r] = int(program_input[program_input_index])

    program_input_index += 1

def mul(left,right):
    global reg
    reg[left] *= right

def div(left,right):
    assert right != 0
    global reg
    reg[left] = int(reg[left]/right)

def mod(left,right):
    assert left >= 0
    assert right > 0
    global reg
    reg[left] = reg[left] % right

def eql(left,right):
    global reg
    if reg[left] == right:
        reg[left] = 1
    else:
        reg[left] = 0

def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    for line in rlines:
        line = line.strip()
        if line == "":
            continue

        s = line.split(" ")
        instr = s[0]
        left = s[1]
        right = parse_right(s)

        if instr == "inp":
            inp(left)
        elif instr == "add":
            add(left, right)
        elif instr == "mul":
            mul(left, right)
        elif instr == "div":
            div(left, right)
        elif instr == "mod":
            mod(left, right)
        elif instr == "eql":
            eql(left, right)
        else:
            assert False

def main():
    parse()
    print(reg)

main()
