from typing import List, Counter

from src.poker import Rank, PokerCard


def is_royal_flush(ranks: List[Rank]) -> bool:
    # 定义皇家同花顺的标准顺序
    royal_flush_ranks = [Rank.A, Rank.K, Rank.Q, Rank.J, Rank.TEN]

    # 逐个比较两个列表的元素
    return all(r1 == r2 for r1, r2 in zip(ranks, royal_flush_ranks))


def sort_hand_card(cards: List[PokerCard]) -> List[PokerCard]:
    """
    对牌型进行排序，排序规则如下：
    1. Rank出现的次数降序排列
    2. Rank的大小降序排列
    3. 相同Rank时按Suit升序排列
    """
    rank_counter = Counter[Rank](card.rank for card in cards)

    return sorted(cards, key=lambda card: (
        -rank_counter[card.rank],  # 按 Rank 出现的次数降序
        -card.rank.value,  # 按 Rank 大小降序
        card.suit,  # 按 Suit 升序
    ))
