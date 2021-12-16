import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
s = ""
version_sum = 0
depth =-1 

# prints p with indent
def pprint(p):
    s = ""
    for i in range(depth):
        s += "   "

    s += p
    #print(s)

# converts hex char to string of exactly 4 binary
def char2bin(c):
    i = int(c, 16)
    b = str(bin(i))[2:]
    s = ""
    for i in range(4-len(b)):
        s += "0"
    s += b
    return s

# returns version,type of s
def vertype(s):
    ver = int(s[0:3],2)
    global version_sum
    version_sum += ver

    t = int(s[3:6],2)
    s = s[6:]
    return s,ver,t

# parses a literal
def literal(s):
    lit = ""
    while True:
        more = int(s[0])
        lit += s[1:5]
        s = s[5:]
        if more == 0:
            break

    lit = int(lit,2)
    pprint("literal " + str(lit))
    return s, lit

# parses operator
# returns remaining string, packets read
def operator(t, s):
    length_id = s[0]
    s = s[1:]

    data = []

    if length_id == "0":
        # length in bits
        length_bits = int(s[0:15], 2)
        pprint("length_bits " + str(length_bits))
        s = s[15:]
        pprint(s)

        start_len = len(s)

        while start_len - len(s) < length_bits:
            s,read = packet(s)
            data.append(read)

        pprint("finished, remainder " + s)
        
    else:
        # number of packets
        length_packets = int(s[0:11], 2)
        pprint("length_packets " + str(length_packets))
        s = s[11:]
        pprint(s)

        packets_read = 0
        while packets_read < length_packets:
            s,read = packet(s)
            data.append(read)
            packets_read += 1

    result = 0

    if t == 0:
        result = sum(data)
    elif t == 1:
        result = data[0]
        for v in data[1:]:
            result *= v
    elif t == 2:
        result = min(data)
    elif t == 3:
        result = max(data)
    elif t == 5:
        if len(data) != 2:
            raise "wrong length for type 5 packet"
        if data[0] > data[1]:
            result = 1
        else:
            result = 0
    elif t == 6:
        if len(data) != 2:
            raise "wrong length for type 6 packet"
        if data[0] < data[1]:
            result = 1
        else:
            result = 0
    elif t == 7:
        if len(data) != 2:
            raise "wrong length for type 6 packet"
        if data[0] == data[1]:
            result = 1
        else:
            result = 0
    else:
        raise "unrecognized type " + t

    return s,result

# parses a random packet starting at s
def packet(s):
    global depth
    depth += 1

    s,ver,t = vertype(s)
    pprint("--- version " + str(ver) + " type " + str(t) + "---")

    result = 0

    if t == 4:
        s,result = literal(s)
    else:
        s,result = operator(t, s)

    depth -= 1

    return s,result

def evaluate(line):
    s = ""

    for c in line:
        s += char2bin(c)

    s,result = packet(s)
    return result

def parse():
    global s

    data = open("data.txt", "r")
    rlines = data.readlines()

    line = rlines[0].strip()
    print("evaluate", evaluate(line))

def test():
    if evaluate("C200B40A82") != 3:
        print("failed C200B40A82")

    if evaluate("04005AC33890") != 54:
        print("failed 04005AC33890")

    if evaluate("880086C3E88112") != 7:
        print("failed 880086C3E88112")

    if evaluate("CE00C43D881120") != 9:
        print("failed CE00C43D881120")

    if evaluate("D8005AC2A8F0") != 1:
        print("failed D8005AC2A8F0")

    if evaluate("F600BC2D8F") != 0:
        print("failed F600BC2D8F")

    if evaluate("9C005AC2F8F0") != 0:
        print("failed 9C005AC2F8F0")

    if evaluate("9C0141080250320F1802104A08") != 1:
        print("failed 9C0141080250320F1802104A08")

def main():
    parse()
    test()

main()


