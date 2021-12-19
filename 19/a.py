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
        dim = [[],[]]
        for x,y in self.beacons:
            dim[0].append(x)
            dim[1].append(y)
        dim[0].sort()
        dim[1].sort()

        # compute deltas
        for i in range(len(dim)):
            delta_dim = []
            dc = dim[i][0]
            for pos in dim[i][1:]:
                delta_dim.append(pos - dc)
                dc = pos

            self.deltas.append(delta_dim)

    # matches other deltas, against all deltas for all dimensions on this scanner
    def match_deltas(self, other):
        # todo: need to pick a few starting candidates from each side and score individually

        # count of matches
        count = [0,0]

        for i in range(len(self.deltas)):
            lhs = self.deltas[i]
            rhs = other.deltas[i]

            # current indices being compared
            left_i = 0
            right_i = 0

            while left_i < len(lhs) and right_i < len(rhs):
                if lhs[left_i] == rhs[right_i]:
                    count[i] += 1
                    left_i += 1
                    right_i += 1

                # todo: handle case where there are bonus points: sum deltas, max lookahead distance, only increment 1 index

            # todo: repeat for permutations of other deltas
            # todo: note that one of the permutations should be delta list reversed
            # ensure len(permutations) == 24

        # todo: column permutations

        # todo: imagine a perfect 1:1 match, with same orientation..
        if count == [2,2]:
            xl,yl = self.beacons[0]
            xr,yr = self.beacons[1]
            transform = (xl -xr, yl - yr)

        return count, transform

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
