#!/usr/bin/env python

from collections import deque
from aocd import get_data, submit

print("\033[2J\033[H") # ]]

data = get_data(year=2020, day=22, block=True)
# data = """
# Player 1:
# 9
# 2
# 6
# 3
# 1

# Player 2:
# 5
# 8
# 4
# 7
# 10
# """.strip()
# data = """
# Player 1:
# 43
# 19

# Player 2:
# 2
# 29
# 14
# """.strip()

p1, p2 = data.split("\n\n")

p1_deck = deque([int(n) for n in p1.splitlines()[1:]])
p2_deck = deque([int(n) for n in p2.splitlines()[1:]])

p1_deck.reverse()
p2_deck.reverse()

def combat(p1_deck, p2_deck):
    while p1_deck and p2_deck:
        if p1_deck[-1] > p2_deck[-1]:
            p1_deck.rotate()
            p1_deck.appendleft(p2_deck.pop())
        else:
            p2_deck.rotate()
            p2_deck.appendleft(p1_deck.pop())
    return p1_deck or p2_deck

gid = 1
def recursive_combat(p1_deck, p2_deck):
    global gid
    print()
    print(f"=== Game {gid} ===")
    print()
    d = [p1_deck, p2_deck]
    rid = 1
    hhist = set()
    while d[0] and d[1]:
        # Lazy way to keep history
        hid = (hash(tuple(p1_deck)), hash(tuple(p2_deck)))
        if hid in hhist:
            print(f"Player 0 wins game {gid} to stop infinite games!")
            return 0
        hhist.add(hid)

        print(f"--- Round {rid} (Game {gid}) ---")
        print(f"Player 1's deck: {', '.join(map(str, reversed(p1_deck)))}")
        print(f"Player 2's deck: {', '.join(map(str, reversed(p2_deck)))}")
        draws = [p1_deck.pop(), p2_deck.pop()]
        print(f"Player 1 plays: {draws[0]}")
        print(f"Player 2 plays: {draws[1]}")
        if draws[0] <= len(p1_deck) and draws[1] <= len(p2_deck):
            print("Playing a sub-game to determine the winner...")
            np1 = list(p1_deck)[-draws[0]:]
            np2 = list(p2_deck)[-draws[1]:]
            gid += 1
            widx = recursive_combat(deque(np1), deque(np2))
            gid -= 1
            print(f"Player {widx+1} wins round {rid} of game {gid}!")
        else:
            widx = 0 if draws[0] > draws[1] else 1
            print(f"Player {widx+1} wins round {rid} of game {gid}!")
        winner = d[widx]
        winner.appendleft(draws.pop(widx))
        winner.appendleft(draws[0])
        print()
        rid += 1

    winner = 0 if p1_deck else 1
    print(f"Player {winner} wins game {gid}!")
    return winner

def score(deck):
    s = 0
    for i, n in enumerate(deck):
        s += (i+1)*n
    return s

d = [p1_deck, p2_deck]
winner = recursive_combat(p1_deck, p2_deck)
print(score(d[winner]))
