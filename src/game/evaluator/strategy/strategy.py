from abc import ABC, abstractmethod
from typing import List, Tuple

from src.game.evaluator.hand_ranking import HandRanking
from src.poker import PokerCard


class HandRankingEvaluateStrategy(ABC):
    """评估策略的抽象基类"""

    @abstractmethod
    def get_hand_rank(self, cards: List[PokerCard]) -> HandRanking:
        """根据给定的五张牌返回牌型"""
        pass

    @abstractmethod
    def get_best_hand_from_seven(self, cards: List[PokerCard]) -> Tuple[HandRanking, List[PokerCard]]:
        """从七张牌中选出最佳的五张牌和相应的牌型"""
        pass
