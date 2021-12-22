import collections

cache = dict()

# returns (p1 wins, p2 wins)
def recurse(rolls, pos, score, turn):
    global cache
    key = (pos[0], score[0], pos[1], score[1], turn)

    if key in cache:
        return cache[key]

    if score[0] >= 21:
        return (1,0)
    if score[1] >= 21:
        return (0,1)

#    print("recurse", score, rolls)

    initial_pos = pos[turn]
    initial_score = score[turn]
    next_turn = (turn + 1) % 2

    p1wins = p2wins = 0

    for i in range(3):
        for j in range(3):
            for k in range(3):
                roll = i + j + k + 3
                rolls.append(roll)

                pos[turn] = initial_pos + roll
                while pos[turn] > 10:
                    pos[turn] -= 10

                score[turn] = initial_score + pos[turn]

                p1call,p2call = recurse(rolls,pos, score, next_turn)

                p1wins += p1call
                p2wins += p2call

                rolls.pop()

    pos[turn] = initial_pos
    score[turn] = initial_score

    value = (p1wins,p2wins)
    cache[key] = value
    
    return value

def main():
    # example: pos = [4, 8]
    #pos = [1,1]
    # data: 
    pos = [7, 9]
    score = [0, 0]

    v = recurse(collections.deque([]), pos, score, 0)
    print("v", v )

main()
