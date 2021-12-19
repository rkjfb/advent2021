import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state
scanner = []
class Scanner:
    def __init__(self, beacons):
        self.beacons = beacons
        self.deltas = []
        self.compute_deltas()

    # computes positive deltas between sorted coordinates, per dimension
    def compute_deltas(self):
        # get a sorted list of 1 dimension
        dim = []
        for x,y in self.beacons:
            dim.append(x)
        dim.sort()

        # compute deltas
        delta_dim = []
        dc = dim[0]
        for i in dim[1:]:
            delta_dim.append(i - dc)
            dc = i

        self.deltas.append(delta_dim)

        # todo: repeat for other dimensions

    # matches rhs delta (for a single dimension), against all deltas for all dimensions on this scanner
    def match_deltas(self, other):
        # todo: need to pick a few starting candidates from each side and score individually

        lhs = self.deltas[0]
        rhs = other.deltas[0]

        # current indices being compared
        left_i = 0
        right_i = 0

        # count of matches
        count = 0 

        while left_i < len(lhs) and right_i < len(rhs):
            if lhs[left_i] == rhs[right_i]:
                count += 1
                left_i += 1
                right_i += 1

            # todo: handle case where there are bonus points: sum deltas, max lookahead distance, only increment 1 index

        # todo: repeat for other deltas on this scanner

        return count

def parse():
    global scanner

    data = open("data.txt", "r")
    rlines = data.readlines()

    current = None

    beacons = []

    for line in rlines:
        line = line.strip()
        if line == "":
            continue

        if line[1] == "-":
            if len(beacons) > 0:
                scanner.append(Scanner(beacons))
                beacons = []
        else:
            s = line.split(",")
            beacons.append((int(s[0]),int(s[1])))

    scanner.append(Scanner(beacons))

def main():
    parse()
    print(scanner)

    print("scan match count", scanner[0].match_deltas(scanner[1]))

main()
