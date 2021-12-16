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
    print(s)

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
    return s, 1

# parses operator
# returns remaining string, packets read
def operator(s):
    length_id = s[0]
    s = s[1:]

    packets_read = 0

    if length_id == "0":
        # length in bits
        length_bits = int(s[0:15], 2)
        pprint("length_bits " + str(length_bits))
        s = s[15:]
        pprint(s)

        start_len = len(s)

        while start_len - len(s) < length_bits:
            s,read = packet(s)
            packets_read += 1

        pprint("finished, remainder " + s)
        
    else:
        # number of packets
        length_packets = int(s[0:11], 2)
        pprint("length_packets " + str(length_packets))
        s = s[11:]
        pprint(s)

        while packets_read < length_packets:
            s,read = packet(s)
            packets_read += 1
            pprint("packets_read " + str(packets_read))

    return s,packets_read

# parses a random packet starting at s
def packet(s):
    global depth
    depth += 1

    s,ver,t = vertype(s)
    pprint("--- version " + str(ver) + " type " + str(t) + "---")

    packets_read = 0

    if t == 4:
        s,packets_read = literal(s)
    else:
        s,packets_read = operator(s)

    depth -= 1

    return s,packets_read

def parse():
    global s

    data = open("data.txt", "r")
    rlines = data.readlines()

    line = rlines[0].strip()

    s = ""

    for c in line:
        s += char2bin(c)

    pprint(s)

    packet(s)

    print("** version_sum", version_sum)


def main():
    parse()

main()


