import re
import json
import copy
#import numpy as np
import collections
import math

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None

    def magnitude(self):
        left = self.left
        if isinstance(self.left, Node):
            left = self.left.magnitude()

        right = self.right
        if isinstance(self.right, Node):
            right = self.right.magnitude()

        return 3*left + 2*right

    # walk tree, inorder, calling func with node and data
    # func returns False to end walk
    def traverse(self, func, data, depth = 1, reverse = False):
        visit = []
        if isinstance(self.left, Node):
            visit.append(self.left)
        else:
            visit.append(None)

        if isinstance(self.right, Node):
            visit.append(self.right)
        else:
            visit.append(None)

        if reverse:
            visit.reverse()

        if visit[0] != None:
            if not visit[0].traverse(func, data, depth+1, reverse):
                return False

        if not func(self, data, depth):
            return False

        if visit[1] != None:
            if not visit[1].traverse(func, data, depth+1, reverse):
                return False

        return True

    def __repr__(self):
        return "[" + str(self.left) + "," + str(self.right) + "]"

# useful problem state
rows = []

# returns a Node, remaining s
def recurse_parse(s):
    if s[0] != "[":
        raise "bad parse"

    s = s[1:]

    n = Node()

    if s[0] in "0123456789":
        n.left = int(s[0])
        # 4,
        s = s[2:]
    elif s[0] == "[":
        n.left,s = recurse_parse(s)
        n.left.parent = n
        # ,
        s = s[1:]
    else:
        raise "unexpected char" 

    if s[0] in "0123456789":
        n.right = int(s[0])
        # 4]
        s = s[2:]
    elif s[0] == "[":
        n.right,s = recurse_parse(s)
        n.right.parent = n
        # ]
        s = s[1:]
    else:
        raise "unexpected char: "

    return n,s

# callback for finding first depth=5 node
def find_explode(n, hit_list, depth):
    if depth == 5:
        hit_list.append(n)
        return False

    return True

# callback for explode next add
def explode_next(n, state, depth):

    if state["target"] == n:
        state["hitnext"] = True
        return True

    if state["hitnext"]:
        if isinstance(n.left, int):
            n.left += state["value"]
            return False
        elif isinstance(n.right, int):
            n.right += state["value"]
            return False

    return True

# callback for explode prev add
def explode_prev(n, state, depth):

    if state["target"] == n:
        state["hitprev"] = True
        return True

    if state["hitprev"]:
        if isinstance(n.right, int):
            n.right += state["value"]
            return False
        elif isinstance(n.left, int):
            n.left += state["value"]
            return False

    return True

# returns True if an explode occured
def explode(n):

    hit_list = []
    n.traverse(find_explode, hit_list)
    if len(hit_list) == 0:
        return False
    hit = hit_list[0]

    state = { "target" : hit, "hitnext" : False, "value": hit.right}
    n.traverse(explode_next, state)

    state = { "target" : hit, "hitprev" : False, "value": hit.left}
    n.traverse(explode_prev, state, reverse=True)

    if hit.parent.left == hit:
        hit.parent.left = 0

    if hit.parent.right == hit:
        hit.parent.right = 0

    return True

# callback for split
def find_split(n, hit_list, depth):
    if isinstance(n.left, int) and n.left >= 10:
        new_node = Node()
        new_node.left = int(math.floor(n.left / 2))
        new_node.right = int(math.ceil(n.left / 2))
        new_node.parent = n
        n.left = new_node
        hit_list.append(True)
        return False

    if isinstance(n.right, int) and n.right >= 10:
        new_node = Node()
        new_node.left = int(math.floor(n.right / 2))
        new_node.right = int(math.ceil(n.right / 2))
        new_node.parent = n
        n.right = new_node
        hit_list.append(True)
        return False

    return True
# returns True if a split occured
def split(n):
    hit_list = []
    n.traverse(find_split, hit_list)

    if len(hit_list) > 0 and hit_list[0]:
        return True

    return False

# reduces n
def reduce(n):
    while True:
        if explode(n):
            #print("explode", n)
            continue
        if split(n):
            #print("split  ", n)
            continue

        break

# adds 2 nodes
def add(left, right):
    root = Node()
    root.left = left
    left.parent = root
    root.right = right
    right.parent = root

    reduce(root)

    return root

def parse():
    global rows

    data = open("data.txt", "r")
    rlines = data.readlines()

    current = None

    for line in rlines:
        line = line.strip()
        n,s = recurse_parse(line)
        rows.append(n)


def test_explode_instance(test, expect):
    n,s = recurse_parse(test)
    explode(n)
    if str(n) != expect:
        print("failed explode test", test, "got", n, "expected", expect)

def test_explode():
    test_explode_instance("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]") # (the 9 has no regular number to its left, so it is not added to any regular number).
    test_explode_instance("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]") # (the 2 has no regular number to its right, and so it is not added to any regular number).
    test_explode_instance("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]")
    test_explode_instance("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") # (the pair [3,2] is unaffected because the pair [7,3] is further to the left; [3,2] would explode on the next action).
    test_explode_instance("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")

def test_magnitude_instance(test, val):
    n,s = recurse_parse(test)
    mag = n.magnitude()
    if str(mag) != val:
        print("failed magnitude", test, "got", mag, "expected", val)

def test_magnitude():
    test_magnitude_instance("[[1,2],[[3,4],5]]", "143")
    test_magnitude_instance("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", "1384")
    test_magnitude_instance("[[[[1,1],[2,2]],[3,3]],[4,4]]", "445")
    test_magnitude_instance("[[[[3,0],[5,3]],[4,4]],[5,5]]", "791")
    test_magnitude_instance("[[[[5,0],[7,4]],[5,5]],[6,6]]", "1137")
    test_magnitude_instance("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", "3488")

def max_pair():
    maxpair = 0
    for i in range(len(rows)):
        for j in range(len(rows)):
            if i == j:
                continue

            a = copy.deepcopy(rows[i])
            b = copy.deepcopy(rows[j])
            result = add(a,b)
            result_mag = result.magnitude()

            if result_mag > maxpair:
                maxpair = result_mag

    print("maxpair", maxpair)
    assert maxpair == 4583

def main():
    test_explode()
    test_magnitude()
    parse()
    max_pair()

main()


