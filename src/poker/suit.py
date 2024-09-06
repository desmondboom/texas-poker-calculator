from enum import Enum
from functools import total_ordering


@total_ordering
class Suit(Enum):
    """扑克牌的花色"""
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3

    def symbol(self):
        symbols = ['♥', '♦', '♣', '♠']
        return symbols[self.value]

    def __lt__(self, other):
        if isinstance(other, Suit):
            return self.value < other.value
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Suit):
            return self.value == other.value
        return NotImplemented

    def __hash__(self):
        return hash(self.value)

    def __deepcopy__(self, memo):
        return self
