import re
import json
import copy
#import numpy as np
import collections
import math

# useful problem state

def openb(a):
    return a in "([{<"

def close(a):
    return a in ")]}>"

def balance(a):
    if a == "(":
        return ")"
    if a == "[":
        return "]"
    if a == "{":
        return "}"
    if a == "<":
        return ">"

    raise "fail"

def score(a):
    if a == ")":
        return 1
    if a == "]":
        return 2
    if a == "}":
        return 3
    if a == ">":
        return 4

    raise "fail"


def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    scores = []

    for line in rlines:
        line = line.strip()
        stack = []
        skip = False
        for c in line:
            if openb(c):
                stack.append(c)
            else:
                if balance(stack[-1]) == c:
                    stack.pop()
                else:
                    skip = True
                    break

        if skip:
            continue

        local_score = 0
        stack.reverse()
        for s in stack:
            local_score = 5 * local_score + score(balance(s))

        scores.append(local_score)

    scores.sort()
    print("middle", scores[len(scores)//2])


def main():
    parse()

main()


