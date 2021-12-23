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
        self.link = []

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
        graph[double] = Node(double)
        graph[name].link.append(graph[double])
        graph[double].link.append(name)

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

def main():
    build_graph(False)
    print_graph()

main()
