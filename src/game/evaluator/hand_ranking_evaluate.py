from typing import List, Tuple

from src.game.evaluator.hand_ranking import HandRanking
from src.game.evaluator.strategy.strategy import HandRankingEvaluateStrategy
from src.poker.poker import PokerCard


class HandEvaluator:
    """手牌评估器, 用于检测一组牌中的牌型是什么"""

    def __init__(self, strategy: HandRankingEvaluateStrategy) -> None:
        self.strategy = strategy
        pass

    def get_hand_rank(self, cards: List[PokerCard]) -> HandRanking:
        """根据给定的五张牌返回牌型"""
        return self.strategy.get_hand_rank(cards)

    def get_best_hand_from_seven(self, cards: List[PokerCard]) -> Tuple[HandRanking, List[PokerCard]]:
        """从七张牌中选出最佳的五张牌和相应的牌型"""
        return self.strategy.get_best_hand_from_seven(cards)
