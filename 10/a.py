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
        return 3
    if a == "]":
        return 57
    if a == "}":
        return 1197
    if a == ">":
        return 25137

    raise "fail"


def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    total_score = 0

    for line in rlines:
        line = line.strip()
        stack = []
        i = 1
        for c in line:
            if openb(c):
                stack.append(c)
            else:
                if balance(stack[-1]) == c:
                    stack.pop()
                else:
                    print("line", line, "index", i, "expect", balance(stack[-1]), "actual", c)
                    total_score += score(c)
                    break
            i += 1

    print("total_score", total_score)


def main():
    parse()

main()


