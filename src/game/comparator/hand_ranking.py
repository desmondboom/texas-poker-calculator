from functools import total_ordering
from typing import List

from src.poker import Rank
from src.game.comparator.hand_rank import HandRank


@total_ordering
class HandRanking:
    """手牌的牌型, 可以用于大小的比较"""
    def __init__(self, rank: HandRank, high_cards: List[Rank]) -> None:
        self.rank = rank  
        self.high_cards = high_cards

    def __lt__(self, other: 'HandRanking') -> bool:
        if self.rank == other.rank:
            return self.high_cards < other.high_cards
        return self.rank < other.rank

    def __eq__(self, other: 'HandRanking') -> bool:
        return self.rank == other.rank and self.high_cards == other.high_cards

    def __repr__(self) -> str:
        return f"HandRanking(rank={self.rank}, high_cards={[str(card) for card in self.high_cards]})"
    