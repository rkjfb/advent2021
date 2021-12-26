import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation
import sys

# graph of board paths
graph = {}
hallway_nodes = set()
room_nodes = set()
# current board state
state = {}

class Node():
    def __init__(self, name):
        self.name = name

        # links to neighbours
        self.link = []

        # value must only be this value
        self.restricted = None

    def value(self):
        global state
        return state.get(self.name, None)

    def set_value(self, val):
        global state
        state[self.name] = val

    # returns (True, score) if there's a path to target
    # otherwise (False, 0)
    def path_to(self, target):
        #print(f"{self.name} path_to {target.name}")
        if target.restricted != None:
            if self.value() != target.restricted:
                # eg. only D is allowed in 'dd'
                return (False,0)

        step_cost_dict = {"A":1, "B":10, "C":100, "D":1000}
        step_cost = step_cost_dict[self.value()]

        visited = set([self])
        explore = []
        for t in self.link:
            if t.value() == None:
                multiplier = 1
                if t.name in hallway_nodes or self.name in hallway_nodes:
                    # todo: technically incorrect for ll and rr
                    multiplier = 2
                explore.append((t, multiplier*step_cost))
                visited.add(t)

        while len(explore) > 0:
            (n, current_cost) = explore.pop()
            #print(f"visit {n.name} {current_cost}")

            if n == target:
                return (True, current_cost)

            for t in n.link:
                if t.value() == None and not t in visited:
                    multiplier = 1
                    if t.name in hallway_nodes or n.name in hallway_nodes:
                        if t.name not in ["ll", "rr"]:
                            multiplier = 2
                    explore.append((t, current_cost+multiplier*step_cost))
                    visited.add(t)

        return (False,0)

    # moves contents of self to target
    def move_to(self, target):
        (exists,cost) = self.path_to(target)
        if not exists:
            print(f"no path_to from {self.name}:{self.value()} to {target.name}")
            print_graph()
            assert False
        assert target.value() == None
        if self.value() == None:
            print(f"asked to move None: from {self.name}:{self.value()} to {target.name}:{target.value()}")
            print_graph()
            assert False


        target.set_value(self.value())
        self.set_value(None)

    # returns all legal moves
    # [(from_key,to_key,cost)]
    def all_legal_moves(self):
        if self.value() == None:
            print(f"all_legal_moves {self.name}:{self.value()}")
            print_graph()
            assert False

        target_set = None
        if self.name in hallway_nodes:
            target_set = room_nodes
        else:
            target_set = hallway_nodes

        ret = []
        for target_name in target_set:
            target = graph[target_name]
            (exists, cost) = self.path_to(target)
            if exists:
                ret.append((self.name, target.name, cost))

        return ret

def build_graph(example):
    global graph
    global hallway_nodes
    global room_nodes

    top_names = ["ll", "l", "ab", "bc", "cd", "r", "rr"]
    hallway_nodes = set(top_names)

    # create the top row nodes
    for name in top_names:
        assert name in hallway_nodes
        graph[name] = Node(name)

    # link top row
    for i in range(len(top_names)-1):
        graph[top_names[i]].link.append(graph[top_names[i+1]])
        graph[top_names[i+1]].link.append(graph[top_names[i]])

    # create bottom 4 row nodes
    # link bottom with middle
    bot_names = ["a", "b", "c", "d"]
    for name in bot_names:
        graph[name] = Node(name)
        graph[name].restricted = name.upper()

        double = name+name
        graph[double] = Node(double)
        graph[double].restricted = name.upper()
        graph[name].link.append(graph[double])
        graph[double].link.append(graph[name])

        triple = double+name
        graph[triple] = Node(triple)
        graph[triple].restricted = name.upper()
        graph[double].link.append(graph[triple])
        graph[triple].link.append(graph[double])

        quad = triple+name
        graph[quad] = Node(quad)
        graph[quad].restricted = name.upper()
        graph[triple].link.append(graph[quad])
        graph[quad].link.append(graph[triple])


    # link middle to top 2
    for i in range(len(bot_names)):
        bot = bot_names[i]

        top = top_names[i+1]
        graph[bot].link.append(graph[top])
        graph[top].link.append(graph[bot])

        top2 = top_names[i+2]
        graph[bot].link.append(graph[top2])
        graph[top2].link.append(graph[bot])

    # clear initial state
    for k,v in graph.items():
        state[k] = None
        room_nodes.add(k)

    room_nodes = room_nodes - hallway_nodes

    # problem-specific state
    state["aa"] = "D"
    state["bb"] = "C"
    state["cc"] = "B"
    state["dd"] = "A"

    state["aaa"] = "D"
    state["bbb"] = "B"
    state["ccc"] = "A"
    state["ddd"] = "C"
    if example:
        state["a"] = "B"
        state["b"] = "C"
        state["c"] = "B"
        state["d"] = "D"

        state["aaaa"] = "A"
        state["bbbb"] = "D"
        state["cccc"] = "C"
        state["dddd"] = "A"
    else:
        state["a"] = "D"
        state["b"] = "B"
        state["c"] = "C"
        state["d"] = "A"

        state["aaaa"] = "C"
        state["bbbb"] = "A"
        state["cccc"] = "D"
        state["dddd"] = "B"

def print_graph():
    row = ""
    top_names = ["ll", "l", "ab", "bc", "cd", "r", "rr"]
    for name in top_names:
        if graph[name].value() == None:
            row += "."
        else:
            row += graph[name].value()

        if name in ["l", "ab", "bc", "cd"]:
            row += "."

    print(row)

    row2 = "  "
    row3 = "  "
    row4 = "  "
    row5 = "  "
    bot_names = ["a", "b", "c", "d"]
    for name in bot_names:
        if graph[name].value() == None:
            row2 += "."
        else:
            row2 += graph[name].value()
        row2 += " "

        double = name+name
        if graph[double].value() == None:
            row3 += "."
        else:
            row3 += graph[double].value()
        row3 += " "

        triple = double+name
        if graph[triple].value() == None:
            row4 += "."
        else:
            row4 += graph[triple].value()
        row4 += " "

        quad = triple+name
        if graph[quad].value() == None:
            row5 += "."
        else:
            row5 += graph[quad].value()
        row5 += " "

    print(row2)
    print(row3)
    print(row4)
    print(row5)

# returns a final move it if exists
# (startposkey, endposkey)
def find_final_move():
    for k,v in state.items():
        if v == None:
            continue

        c = v.lower()
        double = c + c
        triple = double + c
        quad = triple + c

        targets = [quad,triple,double,c]

        for t in targets:
            if state[t] == None:
                (exists,cost) = graph[k].path_to(graph[t])
                if exists:
                    return (k, t, cost)
            if state[t] != v:
                # don't have a final move if lower layer isn't correct
                return None

    return None

# return the list of legal clear out moves
# a clear out move pushes a value from a final spot it should not be in
# [(startposkey, endposkey)]
def build_clearout_moves():
    moves = []

    priority = [ "d", "c", "b", "a"]

    for c in priority:
        upper = c.upper()

        double = c + c
        triple = double + c
        quad = triple + c

        targets = [quad,triple,double,c]

        # start clearout at first unmatched target
        start_clearout_index = 0
        while start_clearout_index < len(targets) and state[targets[start_clearout_index]] in [upper,None]:
            start_clearout_index += 1

        for i in range(start_clearout_index, len(targets)):
            if state[targets[i]] != None:
                clear_list = graph[targets[i]].all_legal_moves()
                moves.extend(clear_list)

    return moves

# builds a list of all legal moves for the current board
def build_moves():
    move = find_final_move()
    if move != None:
        # if there is a final move, just do it
        return [move]

    moves = build_clearout_moves()

    #print(moves)

    # todo: are there more legal moves here?

    return moves

# returns True if the puzzle is solved
def finished():
    priority = [ "d", "c", "b", "a"]

    for c in priority:
        double = c + c
        upper = c.upper()

        if state[c] != upper or state[double] != upper:
            return False

    return True

iterations = 0
min_solved_cost = 999999
min_solved_steps = []

# return True if problem is solved
def recurse_solve(steps, depth, start_cost):
    global min_solved_cost
    global min_solved_steps

    if finished():
        if start_cost < min_solved_cost:
            min_solved_cost = start_cost
            min_solved_steps = steps.copy()
            print("solved, new min_solved_cost", min_solved_cost, len(steps))
        return True

    if start_cost > min_solved_cost:
        # no need to keep searching if we're on a more expensive path than already solved
        return False

    moves = build_moves()
    if len(moves) == 0:
        return False

    global iterations
    iterations += 1
    if iterations > 10000:
        return False

    if iterations % 100 == 0:
        print("iterations", iterations)
        print_graph()

    if depth == 3 and False:
        print("depth", depth, "start_cost", start_cost, "moveslen", len(moves))
        print("moves", moves)
        print_graph()
        assert False

    ret_solved = False

    for from_k,to_k,move_cost in moves:
        backup_from = state[from_k]
        backup_to = state[to_k]
        steps.append((from_k,to_k,move_cost))

        graph[from_k].move_to(graph[to_k])

        if from_k == "dddd":
            print("clearing dddd", iterations)
            print_graph()
            assert False

        solved = recurse_solve(steps, depth+1, start_cost+move_cost)

        if solved:
            ret_solved = True

        steps.pop()
        state[from_k] = backup_from
        state[to_k] = backup_to

    return ret_solved

def main():
    build_graph(True)
    print_graph()

#    print("all_legal_moves aa")
#    moves = graph["a"].all_legal_moves()
#    for m in moves:
#        print(m)

    solved = recurse_solve([], 0, 0)
    print("solved", solved, iterations)
    print("min_solved_cost", min_solved_cost)

    total = 0
    for from_k, to_k, cost in min_solved_steps:
        graph[from_k].move_to(graph[to_k])
        print(f"{total}+{cost} {graph[to_k].value()} to {to_k}")
        total += cost
        print_graph()

main()
