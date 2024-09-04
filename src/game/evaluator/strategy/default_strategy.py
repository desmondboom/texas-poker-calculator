from itertools import combinations
from typing import List, Tuple

from src.game.evaluator.hand_rank import HandRank
from src.game.evaluator.hand_ranking import HandRanking
from src.game.evaluator.strategy.utils import is_royal_flush, sort_hand_card
from src.game.evaluator.strategy.strategy import HandRankingEvaluateStrategy
from src.poker import PokerCard


class DefaultHandRankingEvaluateStrategy(HandRankingEvaluateStrategy):
    """默认的评估策略"""

    def __init__(self) -> None:
        super().__init__()

    def get_best_hand_from_seven(self, cards: List[PokerCard]) -> Tuple[HandRanking, List[PokerCard]]:
        """给定七张牌，返回最好的五张牌的 HandRanking 以及组成该牌型的牌"""
        best_hand = None
        best_combination = None

        # 生成所有可能的5张牌组合
        for five_card_combination in combinations(cards, 5):
            # 计算该5张牌的 HandRanking
            current_hand = self.get_hand_rank(list(five_card_combination))

            # 比较当前的 HandRanking 和当前最好的 HandRanking
            if best_hand is None or current_hand > best_hand:
                best_hand = current_hand
                best_combination = list(five_card_combination)

        # 对最好的五张牌进行排序
        best_combination = sort_hand_card(best_combination)

        # 返回最好的 HandRanking 和组成牌型的五张牌
        # for card in best_combination:
        #     print(card.display())
        return best_hand, best_combination

    def get_hand_rank(self, cards: List[PokerCard]) -> HandRanking:
        """给定一组牌(五张)，返回 HandRanking 对象，表示这组牌的牌型和高牌"""

        # 提取所有牌的 Rank（点数），并按从大到小排序，得到 ranks 列表
        ranks = sorted([card.rank for card in cards], reverse=True)

        # 提取所有牌的 Suit（花色），得到 suits 列表
        suits = [card.suit for card in cards]
        # 检查是否为同花，即所有牌的花色是否相同
        is_flush = len(set(suits)) == 1
        # 检查是否为顺子，即所有牌的点数是否连续（这里用 Rank 的数值来判断）
        is_straight = all(ranks[i].value - 1 == ranks[i + 1].value for i in range(len(ranks) - 1))
        # 如果是同花且是顺子，进一步检查是否是皇家同花顺
        if is_flush and is_straight:
            # 检查是否是特定的牌型 A, K, Q, J, 10，这就是皇家同花顺
            if is_royal_flush(ranks):
                return HandRanking(HandRank.ROYAL_FLUSH, ranks)
            # 如果不是皇家同花顺，但仍是同花顺
            return HandRanking(HandRank.STRAIGHT_FLUSH, ranks)
            # 统计每种 Rank（点数）出现的次数，存储在字典 rank_counts 中，键是 Rank，值是出现次数
        rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}

        # 提取 Rank 出现的次数，并按次数从大到小排序，得到 rank_count_values 列表
        rank_count_values = sorted(rank_counts.values(), reverse=True)

        # 按 Rank 的出现次数和点数从大到小对 Rank 进行排序，得到 sorted_ranks_by_count 列表
        sorted_ranks_by_count = sorted(rank_counts.keys(), key=lambda r: (-rank_counts[r], -r.value))
        # 如果有 4 张相同的牌（四条）
        if rank_count_values == [4, 1]:
            return HandRanking(HandRank.FOUR_OF_A_KIND, sorted_ranks_by_count)

        # 如果是三条和一对（满堂红，或称作葫芦）
        if rank_count_values == [3, 2]:
            return HandRanking(HandRank.FULL_HOUSE, sorted_ranks_by_count)

        # 如果是同花（花色相同，但不连续）
        if is_flush:
            return HandRanking(HandRank.FLUSH, ranks)

        # 如果是顺子（点数连续，但花色不同）
        if is_straight:
            return HandRanking(HandRank.STRAIGHT, ranks)

        # 如果有三张相同的牌（三条）
        if rank_count_values == [3, 1, 1]:
            return HandRanking(HandRank.THREE_OF_A_KIND, sorted_ranks_by_count)

        # 如果有两对（两对相同点数的牌）
        if rank_count_values == [2, 2, 1]:
            return HandRanking(HandRank.TWO_PAIR, sorted_ranks_by_count)

        # 如果有一对（两张相同点数的牌）
        if rank_count_values == [2, 1, 1, 1]:
            return HandRanking(HandRank.ONE_PAIR, sorted_ranks_by_count)
            # 如果没有其他更强的牌型，则是高牌
        return HandRanking(HandRank.HIGH_CARD, ranks)
