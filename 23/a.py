import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation

# useful problem state
graph = {}

class Node():
    def __init__(self, name):
        self.name = name
        self.value = None

        # links to neighbours
        self.link = []

        # value must only be this value
        self.restricted = None

    # returns true if there's a path to target
    def path_to(self, target):
        if target.restricted != None:
            if self.value != target.restricted:
                # eg. only D is allowed in 'dd'
                return False

        visited = set()
        explore = []
        for t in self.link:
            if t.value == None:
                explore.append(t)

        while len(explore) > 0:
            n = explore.pop()
            visited.add(n)

            if n == target:
                return True

            for t in n.link:
                if t.value == None and not t in visited:
                    explore.append(t)

        return False

    # moves contents of self to target
    def move_to(self, target):
        if not self.path_to(target):
            print(f"no path_to from {self.name}:{self.value} to {target.name}")
            assert False
        assert target.value == None
        assert self.value != None

        target.value = self.value
        self.value = None

    # tries to empty spot
    def push_out(self):
        # todo: think about pushing out top lane
        # todo: think about favouring outside pushes, with an inside option
        assert self.value != None
        if not self.name in [ "dd", "d", "cc", "c", "bb", "b", "aa", "a" ]:
            assert False

        for t in self.link:
            if t.value == None:
                self.move_to(t)
                return

        # todo: hard coded 0
        self.link[0].push_out()

        print_graph()

        self.move_to(self.link[0])

def build_graph(example):
    global graph

    top_names = ["ll", "l", "ab", "bc", "cd", "r", "rr"]

    for name in top_names:
        graph[name] = Node(name)

    for i in range(len(top_names)-1):
        graph[top_names[i]].link.append(graph[top_names[i+1]])
        graph[top_names[i+1]].link.append(graph[top_names[i]])

    bot_names = ["a", "b", "c", "d"]
    for name in bot_names:
        double = name+name
        graph[name] = Node(name)
        graph[name].restricted = name.upper()
        graph[double] = Node(double)
        graph[double].restricted = name.upper()
        graph[name].link.append(graph[double])
        graph[double].link.append(graph[name])

    # zigs
    for i in range(len(bot_names)):
        bot = bot_names[i]
        top = top_names[i+1]
        top2 = top_names[i+2]
        graph[bot].link.append(graph[top])
        graph[bot].link.append(graph[top2])
        graph[top].link.append(graph[top2])

    if example:
        graph["a"].value = "B"
        graph["aa"].value = "A"
        graph["b"].value = "C"
        graph["bb"].value = "D"
        graph["c"].value = "B"
        graph["cc"].value = "C"
        graph["d"].value = "D"
        graph["dd"].value = "A"
    else:
        graph["a"].value = "D"
        graph["aa"].value = "C"
        graph["b"].value = "B"
        graph["bb"].value = "A"
        graph["c"].value = "C"
        graph["cc"].value = "D"
        graph["d"].value = "A"
        graph["dd"].value = "B"

def print_graph():
    row = ""
    top_names = ["ll", "l", "ab", "bc", "cd", "r", "rr"]
    for name in top_names:
        if graph[name].value == None:
            row += "."
        else:
            row += graph[name].value

        if name in ["l", "ab", "bc", "cd"]:
            row += "."

    print(row)

    row2 = "  "
    row3 = "  "
    bot_names = ["a", "b", "c", "d"]
    for name in bot_names:
        if graph[name].value == None:
            row2 += "."
        else:
            row2 += graph[name].value
        row2 += " "

        double = name+name
        if graph[double].value == None:
            row3 += "."
        else:
            row3 += graph[double].value
        row3 += " "

    print(row2)
    print(row3)


def solve():
    global graph

    priority = [ "dd", "d", "cc", "c", "bb", "b", "aa", "a" ]
    expected = [ "D", "D",  "C", "C",  "B", "B", "A", "A" ]
    for i in range(len(priority)):
        print("iteration", i)
        print_graph()
        # pick the most valuable target first (D in dd)
        current = graph[priority[i]]
        expect = expected[i]
        if current.value == expect:
            # pick a new target
            continue

        # if the target slot is empty, check if we can just move into it
        if current.value == None:
            finished = False
            for k,v in graph:
                if v.value == expect:
                    if v.path_to(current):
                        v.move_to(current)
                        finished = True
                        break
            if finished:
                continue

        # bugbug: we might have space, but not a path to move into..

        # make some space
        current.push_out()

def main():
    build_graph(True)
    solve()
    print_graph()

main()
