from functools import total_ordering
from collections import Counter

with open('day7.txt', 'r') as f:
    data = f.read()

HAND_TYPES = [
    # 5 of a kind
    [5],
    # 4 of a kind
    [1, 4], 
    # Full house
    [2, 3],
    # 3 of a kind
    [1, 1, 3],
    # 2 pair
    [1, 2, 2],
    # 1 pair
    [1, 1, 1, 2],
    # High cards
    [1, 1, 1, 1, 1]
]

def part_one(data):
    @total_ordering
    class Hand:
        def __init__(self, cards: list[str]):
            self.cards = cards
            self.counts = sorted(Counter(cards).values())

        def __lt__(self, other: 'Hand'):
            # Simple case: Their score is strictly larger
            if self.score != other.score:
                return self.score < other.score

            # Complex case, check cards in order to find who has the first card that is larger
            for my_card, their_card in zip(self.cards, other.cards):
                if my_card != their_card:
                    return my_card < their_card

            # Equal
            return False

        def __eq__(self, other: 'Hand'):
            return self.cards == other.cards

        @property
        def score(self):
            for i, l in enumerate(HAND_TYPES):
                if l == self.counts:
                    return len(HAND_TYPES)-i

            # Should be impossible
            assert False

    lines = data.splitlines()

    CARD_LOOKUP = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14,
    }

    game = []
    for line in lines:
        cards, b = line.split()
        hand = Hand([CARD_LOOKUP[c] for c in cards])
        bid = int(b)
        game.append((hand, bid))

    total = 0
    for rank, (hand, bid) in enumerate(sorted(game)):
        total += bid * (rank+1)

    return total

def part_two(data):

    @total_ordering
    class Hand:
        def __init__(self, cards: list[str]):
            self.cards = cards
            counts = Counter(cards)
            jokers = counts.pop(1, 0)
            common = counts.most_common(1)

            if common:
                card, _ = common[0]
                counts[card] += jokers
            else:
                # Oops! All Jokers!
                counts[14] = jokers

            self.counts = sorted(counts.values())

        def __lt__(self, other: 'Hand'):
            # Simple case: Their score is strictly larger
            if self.score != other.score:
                return self.score < other.score

            # Complex case, check cards in order to find who has the first card that is larger
            for my_card, their_card in zip(self.cards, other.cards):
                if my_card != their_card:
                    return my_card < their_card

            # Equal
            return False

        def __eq__(self, other: 'Hand'):
            return self.cards == other.cards

        @property
        def score(self):
            for i, l in enumerate(HAND_TYPES):
                if l == self.counts:
                    return len(HAND_TYPES)-i

            # Should be impossible
            assert False

    lines = data.splitlines()

    CARD_LOOKUP = {
        'J': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'Q': 12,
        'K': 13,
        'A': 14,
    }

    game = []
    for line in lines:
        cards, b = line.split()
        hand = Hand([CARD_LOOKUP[c] for c in cards])
        bid = int(b)
        game.append((hand, bid))

    total = 0
    for rank, (hand, bid) in enumerate(sorted(game)):
        total += bid * (rank+1)

    return total

print(part_one(data))
print(part_two(data))
