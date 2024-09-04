from enum import Enum
from functools import total_ordering


@total_ordering
class HandRank(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    def __eq__(self, other):
        if isinstance(other, HandRank):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, HandRank):
            return self.value < other.value
        return NotImplemented
