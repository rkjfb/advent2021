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

    def __repr__(self):
        return "[" + str(self.left) + "," + str(self.right) + "]"

# useful problem state

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

# returns node to explode or None
def find_explode(n,depth):
    if depth == 5:
        return n

    if isinstance(n.left, Node):
        hit = find_explode(n.left, depth+1)
        if hit != None:
            return hit

    if isinstance(n.right, Node):
        hit = find_explode(n.right, depth+1)
        if hit != None:
            return hit

    return None

explode_prev = None
explode_prev_done = False
explode_hit_next = False
# inorder traversal
def explode_walk(n, hit, leftval, rightval):
    global explode_prev
    global explode_prev_done
    global explode_hit_next

    if isinstance(n.left, Node):
        explode_walk(n.left, hit, leftval, rightval)

    if explode_hit_next:
        if isinstance(n.left, int):
            n.left += rightval
            explode_hit_next = False
        elif isinstance(n.right, int):
            n.right += rightval
            explode_hit_next = False

    if n == hit:

        if explode_prev != None and not explode_prev_done:
            if isinstance(explode_prev.right, int):
                explode_prev.right += leftval
            else:
                if not isinstance(explode_prev.left, int):
                    raise "left must be an int"
                explode_prev.left += leftval

        explode_prev_done = True
        explode_hit_next = True

    if isinstance(n.left, int) or isinstance(n.right, int):
        explode_prev = n

    if isinstance(n.right, Node):
        explode_walk(n.right, hit, leftval, rightval)

# returns True if an explode occured
def explode(n):

    hit = find_explode(n, 1)
    if hit == None:
        return False

    if not isinstance(hit.left, int):
        raise "expected hit.left to be int"
    if not isinstance(hit.right, int):
        raise "expected hit.right to be int"

    # this is disgusting.
    global explode_prev
    explode_prev = None
    global explode_prev_done
    explode_prev_done = False
    global explode_hit_next
    explode_hit_next = False
    explode_walk(n, hit, hit.left, hit.right)

    if hit.parent.left == hit:
        hit.parent.left = 0

    if hit.parent.right == hit:
        hit.parent.right = 0

    return True

# returns node 
def find_explode(n,depth):
    if depth == 5:
        return n

    if isinstance(n.left, Node):
        hit = find_explode(n.left, depth+1)
        if hit != None:
            return hit

    if isinstance(n.right, Node):
        hit = find_explode(n.right, depth+1)
        if hit != None:
            return hit

    return None

# returns True if a split occured
def split(n):

    if isinstance(n.left, int) and n.left >= 10:
        new_node = Node()
        new_node.left = int(math.floor(n.left / 2))
        new_node.right = int(math.ceil(n.left / 2))
        new_node.parent = n
        n.left = new_node
        return True

    if isinstance(n.right, int) and n.right >= 10:
        new_node = Node()
        new_node.left = int(math.floor(n.right / 2))
        new_node.right = int(math.ceil(n.right / 2))
        new_node.parent = n
        n.right = new_node
        return True

    if isinstance(n.left, Node):
        hit = split(n.left)
        if hit:
            return True

    if isinstance(n.right, Node):
        hit = split(n.right)
        if hit:
            return True

    return False

# reduces n
def reduce(n):
    while True:
        if explode(n):
            print("explode", n)
            continue
        if split(n):
            print("split  ", n)
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
    data = open("data.txt", "r")
    rlines = data.readlines()

    current = None

    for line in rlines:
        line = line.strip()

        new_node,s = recurse_parse(line)

        if current != None:
            current = add(current, new_node)
        else:
            current = new_node

        print("current", current)

        if s != "":
            raise "left overs"


def test_explode_instance(test, expect):
    n,s = recurse_parse(test)
    explode(n)
    if str(n) != expect:
        print("failed explode test", test, "got", n, "expected", expect)
    else:
        print("pass", test)

def test_explode():
    test_explode_instance("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]") # (the 9 has no regular number to its left, so it is not added to any regular number).
    test_explode_instance("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]") # (the 2 has no regular number to its right, and so it is not added to any regular number).
    test_explode_instance("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]")
    test_explode_instance("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") # (the pair [3,2] is unaffected because the pair [7,3] is further to the left; [3,2] would explode on the next action).
    test_explode_instance("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")

def main():
    #test_explode()
    parse()

main()


