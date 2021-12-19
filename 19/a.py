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
        # original beacons in scanner space, sorted by z,y,x
        for i in range(2,-1,-1):
            beacons = beacons[beacons[:,i].argsort()]
        self.beacons = beacons

        # list of all rotations applied, sorted by z,y,x
        self.transformed = []
        self.build_transformed()

        # Beacons, in root coordinate system
        self.root_beacons = None
        # Offset used to get beacons into root coordinate system
        self.root_offset = np.array([-9999, -9999, -9999])


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

    # returns True, and updates root_beacons and root_offset
    def match(self, root_beacons):
        for start_i in range(10):
            for t in self.transformed:
                for start_j in range(10):
                    offset = root_beacons[start_i] - t[start_j]

                    i = start_i 
                    j = start_j 
                    count = 0
                    while i < len(root_beacons) and j < len(t) and count < 12:
                        b = t[j] + offset
                        if np.array_equal(root_beacons[i], b):
                            count += 1
                            if count > 1:
                                print(count)
                            i += 1
                            j += 1
                        # x
                        elif root_beacons[i][0] < b[0]:
                            i += 1
                        elif b[0] < root_beacons[i][0]:
                            j += 1
                        # y
                        elif root_beacons[i][1] < b[1]:
                            i += 1
                        elif b[1] < root_beacons[i][1]:
                            j += 1
                        # z
                        elif root_beacons[i][2] < b[2]:
                            i += 1
                        elif b[2] < root_beacons[i][2]:
                            j += 1
                        else:
                            print("root_beacons", root_beacons[i], "b0", b)
                            assert False

                    if count == 12:
                        self.root_offset = offset
                        self.root_beacons = t + offset
                        return True

        return False

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
                scanner.append(Scanner(np.array(beacons)))
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

    print("match", scanner[1].match(scanner[0].beacons))
    print("scanner1 root_beacons", scanner[1].root_beacons)



main()
