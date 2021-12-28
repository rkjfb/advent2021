import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation

# useful problem state
program = []
program_input = "71323"
program_input_index = 0
reg = { "w" : 0, "x" : 0, "y" : 0, "z" : 0 }

def parse_right(r):
    global reg

    if r.isalpha():
        return reg[r]

    return int(r)

def inp(r):
    global program_input
    global program_input_index
    global reg

    reg[r] = int(program_input[program_input_index])

    program_input_index += 1

def add(left,right):
    global reg
    reg[left] += right

def mul(left,right):
    global reg
    reg[left] *= right

def div(left,right):
    assert right != 0
    global reg
    reg[left] = int(reg[left]/right)

def mod(left,right):
    global reg
    assert reg[left] >= 0
    assert right > 0
    reg[left] = reg[left] % right

def eql(left,right):
    global reg
    if reg[left] == right:
        reg[left] = 1
    else:
        reg[left] = 0

def parse():
    global program

    data = open("data.txt", "r")
    rlines = data.readlines()

    first = True
    subprog = []

    for line in rlines:
        line = line.strip()
        if line == "":
            continue

        s = line.split(" ")
        instr = s[0]
        left = s[1]
        right = None
        if len(s) > 2:
            right = s[2]

        if instr == "inp" and not first:
            program.append(subprog)
            subprog = []

        subprog.append((instr,left,right))
        first = False


    program.append(subprog)

def run_program(i):
    global program
    for instr,left,right in program[i]:
        if instr == "inp":
            inp(left)
        elif instr == "add":
            add(left, parse_right(right))
        elif instr == "mul":
            mul(left, parse_right(right))
        elif instr == "div":
            div(left, parse_right(right))
        elif instr == "mod":
            mod(left, parse_right(right))
        elif instr == "eql":
            eql(left, parse_right(right))
        else:
            assert False

        #print(instr,left,right,reg)

def restart(value):
    global program_input
    global program_input_index
    global reg

    program_input = value
    program_input_index = 0
    reg["w"] = 0
    reg["x"] = 0
    reg["y"] = 0
    reg["z"] = 0

# dump all 3-digit inputs
def dump():
    start = 1000
    for i in range(start, 0, -1):
        s = str(i)
        if "0" in s or len(s)<3:
            continue
        restart(s)
        run_program()
        print(s, reg)

def findbreak():
    maxz = 0
    minz = 99999999999999
    #start = 11111111111111
    start = 1111
    i = start
    while i<=9999:
        i += 1
        if i % 10000 == 0:
            print(i)
        s = str(i)
        if "0" in s:
            continue
        restart(s)
        run_program()
        if reg["z"] > maxz:
            print(minz,maxz)
            maxz = reg["z"]
        if reg["z"] < minz:
            minz = reg["z"]
            print(minz,maxz, i)

        if reg["z"] == 0:
            print("accepted", i, reg["z"])

# dict[prog_index]->set() of most (all?) start Z register values that achieve Z=0 for a all input
backward = {}

# end of round 8 only has 70k distinct! :-)
# dict[prog_index]->set() of all end Z register values for all inputs
forward = {}

# populates backward from 13-prog_index, inclusive
def explore_backward(prog_index):
    print("explore_backward")

    global reg
    global backward
    backward[14] = set([0])
    prev_accept = set([0])
    search_range = 26*26*26
    accepted_z = set()
    max_accepted_in = {}
    for pi in range(13,prog_index-1,-1):
        print()
        print("program", pi)
        accepted_z = set()

        for z in range(0, search_range):
            for i in range(1, 10):
                s = str(i)
                restart(s)
                reg["z"] = z

                run_program(pi)

                if reg["z"] in prev_accept:
                    accepted_z.add(z)
                    if not z in max_accepted_in:
                        max_accepted_in[z] = i

        print("accepted_z len", len(accepted_z))
        if len(accepted_z) < 100:
            row = ""
            for z in accepted_z:
                row += str(z) + ":" + str(max_accepted_in[z]) + ", "
            print("candidates z-inputs", row)

        if len(accepted_z) == 0:
            print("failed to find any accepted zs")
            break

        prev_accept = accepted_z
        backward[pi] = accepted_z

# populates forward from 0->prog_index, inclusive
def explore_forward(prog_index):
    print("explore_forward")
        
    global reg
    forward[-1] = set([0])
    start_z = set([0])

    characters = "123456789"

    for pi in range(0, prog_index+1):
        print()
        print("program", pi)
        end_z = set()

        for s in characters:
            for z in start_z:
                restart(s)
                reg["z"] = z
                run_program(pi)
                end_z.add(reg["z"])

        print("end_z len", len(end_z))
        start_z = end_z 
        forward[pi] = end_z

# given a program, starting Z and known accepted Z reg values (backward), search for max characters
def search_forward(prog_index, start_z):
    print("search_forward", prog_index, start_z)
    ret = ""
        
    global reg
    #characters = "987654321"
    characters = "123456789"

    for pi in range(prog_index, len(program)):
        print("program", pi, "start_z", start_z, "possible outputs", len(backward[pi+1]))
        found = False
        for s in characters:
            restart(s)
            reg["z"] = start_z
            run_program(pi)
            if reg["z"] in backward[pi+1]:
                print("character", s, "regz", reg["z"])
                ret += s
                start_z = reg["z"]
                found = True
                break
        if not found:
            print("candidate z", backward[pi+1])
            assert False

    return ret

# given a program, ending at Z, search backward for max characters
def search_backward(prog_index, end_z):
    print("search_backward", prog_index, end_z)
    assert end_z in forward[prog_index]
    ret = ""
        
    global reg
    #characters = "987654321"
    characters = "123456789"

    for pi in range(prog_index, -1, -1):
        print("program", pi, "end_z", end_z, "possible inputs", len(forward[pi-1]))
        found = False
        for s in characters:
            for start_z in forward[pi-1]:
                restart(s)
                reg["z"] = start_z
                run_program(pi)
                if reg["z"] == end_z:
                    print("character", s, "start_z", start_z)
                    ret += s
                    end_z = start_z
                    found = True
                    break
            if found:
                break
        if not found:
            print("couldn't find an acceptable input, map inputs?")
            assert False

    # reverse string, really
    ret = ret[::-1]

    return ret


def main():
    global program
    global reg
    parse()
    print("programs", len(program))

    split_end = 8
    explore_forward(split_end)
    explore_backward(split_end+1)

    # we've found the 1 Z register value, between 8 and 9, that is both achievable and acceptable
    inter = forward[split_end].intersection(backward[split_end+1])
    assert len(inter) == 1
    split_z = next(iter(inter))
    assert split_z == 15

    head = search_backward(split_end, split_z)
    tail = search_forward(split_end+1, split_z)

    model = head+tail

    print("highest model", model)
    # run the model number through the program and we should get 0
    restart(model)
    for pi in range(len(program)):
        run_program(pi)
    assert reg["z"] == 0

main()
