from enum import Enum


class Suit(Enum):
    """扑克牌的花色"""
    HEARTS = ('Hearts', '♥', 1)
    DIAMONDS = ('Diamonds', '♦', 2)
    CLUBS = ('Clubs', '♣', 3)
    SPADES = ('Spades', '♠', 4)

    def __init__(self, label: str, symbol: str, order: int):
        self.label = label
        self.symbol = symbol
        self._value_ = order

    def __lt__(self, other):
        if isinstance(other, Suit):
            return self._value_ < other._value_
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Suit):
            return self._value_ == other._value_
        return NotImplemented

    def __hash__(self):
        return hash(self._value_)
    
    def __deepcopy__(self, memo):
        return self