import re
import json
import copy
#import numpy as np
import collections
import math
#from scipy.spatial.transform import Rotation

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
        if target.restricted != None:
            if self.value() != target.restricted:
                # eg. only D is allowed in 'dd'
                return (False,0)

        step_cost_dict = {"A":1, "B":10, "C":100, "D":1000}
        step_cost = step_cost_dict[self.value()]

        visited = set()
        explore = []
        for t in self.link:
            if t.value() == None:
                explore.append((t, step_cost))

        while len(explore) > 0:
            (n, current_cost) = explore.pop()
            visited.add(n)

            if n == target:
                return (True, current_cost)

            for t in n.link:
                if t.value() == None and not t in visited:
                    explore.append((t, current_cost+step_cost))

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

    # tries to empty spot
    def push_out(self):
        # todo: think about pushing out top lane
        # todo: think about favouring outside pushes, with an inside option
        assert self.value() != None
        if not self.name in [ "dd", "d", "cc", "c", "bb", "b", "aa", "a" ]:
            assert False

        for t in self.link:
            if t.value() == None:
                self.move_to(t)
                return

        # todo: hard coded 0
        self.link[0].push_out()

        print_graph()

        self.move_to(self.link[0])

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

    # create bottom 2 row nodes
    # link bottom with middle
    bot_names = ["a", "b", "c", "d"]
    for name in bot_names:
        double = name+name
        graph[name] = Node(name)
        graph[name].restricted = name.upper()
        graph[double] = Node(double)
        graph[double].restricted = name.upper()
        graph[name].link.append(graph[double])
        graph[double].link.append(graph[name])

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
    if example:
        state["a"] = "B"
        state["aa"] = "A"
        state["b"] = "C"
        state["bb"] = "D"
        state["c"] = "B"
        state["cc"] = "C"
        state["d"] = "D"
        state["dd"] = "A"
    else:
        state["a"] = "D"
        state["aa"] = "C"
        state["b"] = "B"
        state["bb"] = "A"
        state["c"] = "C"
        state["cc"] = "D"
        state["d"] = "A"
        state["dd"] = "B"

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

    print(row2)
    print(row3)

# returns a final move it if exists
# (startposkey, endposkey)
def find_final_move():
    for k,v in state.items():
        if v == None:
            continue

        c = v.lower()
        double = c + c

        if state[double] == None:
            (exists,cost) = graph[k].path_to(graph[double])
            if exists:
                return (k, double, cost)

        if k != double and state[double] == v and state[c] == None:
            (exists, cost) = graph[k].path_to(graph[c])
            if exists:
                return (k, c, cost)

    return None

# return the list of legal clear out moves
# a clear out move pushes a value from a final spot it should not be in
# [(startposkey, endposkey)]
def build_clearout_moves():
    moves = []

    priority = [ "d", "c", "b", "a"]

    for c in priority:
        double = c + c
        upper = c.upper()

        single_clear_needed = False

        if state[double] != upper and state[double] != None:
            single_clear_needed = True
            double_list = graph[double].all_legal_moves()
            moves.extend(double_list)

        if (single_clear_needed or state[c] != upper) and state[c] != None:
            single_list = graph[c].all_legal_moves()
            moves.extend(single_list)

    return moves

# builds a list of all legal moves for the current board
def build_moves():
    move = find_final_move()
    if move != None:
        # if there is a final move, just do it
        return [move]

    moves = build_clearout_moves()

    #print(moves)

    # todo: are there move legal moves here?

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

# return True if problem is solved
def recurse_solve(depth, start_cost):
    global min_solved_cost

    if finished():
        if start_cost < min_solved_cost:
            min_solved_cost = start_cost
            print("solved, new min_solved_cost", min_solved_cost)
        return True

    if start_cost > min_solved_cost:
        # no need to keep searching if we're on a more expensive path than already solved
        return False

    global iterations
    iterations += 1
    if iterations > 1000:
        return False

    moves = build_moves()
    if len(moves) == 0:
        return False
    print("depth", depth, "start_cost", start_cost, "moveslen", len(moves))
    #print_graph()

    ret_solved = False

    for from_k,to_k,move_cost in moves:
        backup_from = state[from_k]
        backup_to = state[to_k]

        graph[from_k].move_to(graph[to_k])

        if state[to_k] == "D":
            print_graph()

        solved = recurse_solve(depth+1, start_cost+move_cost)

        if solved:
            ret_solved = True

        state[from_k] = backup_from
        state[to_k] = backup_to

    return ret_solved

def main():
    build_graph(True)
    print_graph()
    solved = recurse_solve(0, 0)
    print("solved", solved, iterations)
    print("min_solved_cost", min_solved_cost)
    print_graph()

main()
