import re
import json
import copy
import numpy as np
import collections
import math
from scipy.spatial.transform import Rotation

# useful problem state
scanner = []
rotations = []

class Scanner:
    def __init__(self, beacons):
        self.beacons = beacons
        self.transformed = []
        self.build_transformed()

    # build all transformations of beacons, sorted by z,y,x
    def build_transformed(self):
        for r in rotations:
            result = []
            for b in self.beacons:
                result.append(np.dot(r,b))

            # sort by z,y,x
            result = np.array(result)
            for i in range(2,-1,-1):
                # how this sort works:
                # select column i
                # sorts it, produces list of column indices
                # select columns in index order
                result = result[result[:,i].argsort()]

            self.transformed.append(result)

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
            l = [int(s[0]), int(s[1]), int(s[2])]
            beacons.append(np.array(l))

    scanner.append(Scanner(np.array(beacons)))

# builds the list of 24 unique rotations
def build_rotations():
    global rotations

    # produce all x,y,z rotations, convert to matrix, shove in, and out of set
    uniq = set()
    theta_list = [0, 90, 180, 270]

    result = []
    for x in theta_list:
        rx = Rotation.from_rotvec(x * np.array([1,0,0]), degrees=True)
        for y in theta_list:
            ry = Rotation.from_rotvec(y * np.array([0,1,0]), degrees=True)
            for z in theta_list:
                rz = Rotation.from_rotvec(z * np.array([0,0,1]), degrees=True)
                rfinal = rx * ry * rz
                m = rfinal.as_matrix().round().flatten()
                t = tuple(m.tolist())
                uniq.add(t)

    for t in uniq:
        l = list(t)
        a = np.array(l).reshape(3,3)
        rotations.append(a)

    assert len(rotations) == 24

def main():
    build_rotations()
    parse()
    print("len scanner", len(scanner))
    print("scanner1.transformed", scanner[1].transformed)

main()
