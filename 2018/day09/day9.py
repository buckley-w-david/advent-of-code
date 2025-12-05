def scores(players, last_marble):
    scores = [0] * players

    current_marble_idx = 0
    marbles = [0]

    for next_marble in range(1, last_marble+1):
        if next_marble % 23 == 0:
            scores[next_marble %  players] += next_marble
            target_idx = (current_marble_idx - 7) % len(marbles)
            target = marbles.pop(target_idx)
            scores[next_marble %  players] += target
            current_marble_idx = target_idx
        else:
            current_marble_idx = (current_marble_idx+2) % len(marbles)
            marbles.insert(current_marble_idx, next_marble)

    return scores

def part_one():
    return max(scores(486, 70833))

# This is extremely slow
def part_two():
    return max(scores(486, 70833*100))

assert max(scores(10, 1618)) == 8317
assert max(scores(13, 7999)) == 146373
assert max(scores(17, 1104)) == 2764
assert max(scores(21, 6111)) == 54718
assert max(scores(30, 5807)) == 37305

print(part_one())
# print(part_two())
