import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation

# useful problem state
cache = dict()

# returns (p1 wins, p2 wins)
def recurse(rolls, pos, score, turn):
    global cache
    key = (pos[0], score[0], pos[1], score[1], turn)
    print("recurse", rolls, key)

    initial_pos = pos[turn]
    initial_score = score[turn]
    next_turn = (turn + 1) % 2

    p1wins = p2wins = 0

    for i in range(3):
        for j in range(3):
            for k in range(3):
                roll = i + j + k + 3
                pos[turn] = initial_pos + roll
                rolls.append(roll)
                while pos[turn] > 10:
                    pos[turn] -= 10

                score[turn] += pos[turn]

                if score[turn] >= 21:
                    inner_key = (pos[0], score[0], pos[1], score[1], turn)
                    if turn == 0:
                        cache[inner_key] = (1,0)
                        p1wins += 1
                        #print("caching", inner_key, 1, 0)
                    else:
                        cache[inner_key] = (0,1)
                        p2wins += 1
                        #print("caching", inner_key, 0, 1)
                else:
                    p1call,p2call = recurse(rolls,pos, score, next_turn)
                    p1wins += p1call
                    p2wins += p2call
                rolls.pop()

    pos[turn] = initial_pos
    score[turn] = initial_score

    value = (p1wins,p2wins)
    cache[key] = value
    #print("caching", key, value)
    return value

def main():
    # example: 
    pos = [4, 8]
    #pos = [1,1]
    # data: pos = [7, 9]
    score = [0, 0]

    v = recurse(collections.deque([]), copy.copy(pos), score, 0)
    print("v")

    print("total wins", cache[(pos[0], 0, pos[1], 0, 0)])

main()
