# useful problem state

bal = { "(" : ")",
        "[" : "]",
        "{" : "}",
        "<" : ">"}
score = { ")" : 1,
        "]" : 2,
        "}" : 3,
        ">" : 4}

def parse():
    data = open("data.txt", "r")
    rlines = data.readlines()

    scores = []

    for line in rlines:
        line = line.strip()
        stack = []
        skip = False
        for c in line:
            if c in bal:
                stack.append(c)
            else:
                if bal[stack[-1]] == c:
                    stack.pop()
                else:
                    skip = True
                    break

        if skip:
            continue

        local_score = 0
        stack.reverse()
        for s in stack:
            local_score = 5 * local_score + score[bal[s]]

        scores.append(local_score)

    scores.sort()
    print("middle", scores[len(scores)//2])


def main():
    parse()

main()


