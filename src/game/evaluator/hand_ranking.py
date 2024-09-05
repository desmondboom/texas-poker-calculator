from functools import total_ordering
from typing import List

from src.game.evaluator.hand_rank import HandRank
from src.poker import Rank


@total_ordering
class HandRanking:
    """手牌的牌型, 可以用于大小的比较"""

    def __init__(self, ranking: HandRank, high_cards_ranks: List[Rank]) -> None:
        self.ranking = ranking
        self.high_cards_ranks = high_cards_ranks

    def __lt__(self, other: 'HandRanking') -> bool:
        if self.ranking == other.ranking:
            return self.high_cards_ranks < other.high_cards_ranks
        return self.ranking < other.ranking

    def __eq__(self, other: 'HandRanking') -> bool:
        return self.ranking == other.ranking and self.high_cards_ranks == other.high_cards_ranks

    def __repr__(self) -> str:
        return f"HandRanking(rank={self.ranking}, high_cards={[str(card) for card in self.high_cards_ranks]})"
