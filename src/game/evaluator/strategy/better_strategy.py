from collections import Counter
from typing import List, Tuple

from src.game.evaluator.hand_rank import HandRank
from src.game.evaluator.hand_ranking import HandRanking
from src.game.evaluator.strategy.default_strategy import DefaultHandRankingEvaluateStrategy
from src.game.evaluator.strategy.strategy import HandRankingEvaluateStrategy
from src.game.evaluator.strategy.utils import sort_hand_card
from src.poker import PokerCard, Rank, Suit


class BetterHandRankingEvaluateStrategy(HandRankingEvaluateStrategy):
    """默认的评估策略"""

    def __init__(self) -> None:
        super().__init__()

    def get_best_hand_from_seven(self, cards: List[PokerCard]) -> Tuple[HandRanking, List[PokerCard]]:
        """给定七张牌，返回最好的五张牌的 HandRanking 以及组成该牌型的牌"""

        # 按牌的大小降序排序
        sorted_cards: List[PokerCard] = sort_hand_card(cards)

        # 按花色分类
        suits: List[Suit] = [card.suit for card in sorted_cards]
        suit_counts = Counter(suits)

        # 按点数分类
        ranks = [card.rank for card in sorted_cards]
        rank_counts = Counter(ranks)

        # 查找可能的同花牌
        is_flash = False
        flush_cards = []
        for suit, count in suit_counts.items():
            if count >= 5:
                is_flash = True
                flush_cards = [card for card in sorted_cards if card.suit == suit][:5]
                break

        # 查找顺子
        is_straight = False
        straight_high_card = None
        rank_sequence = sorted(set(ranks), reverse=True)
        print(rank_sequence)
        for start_index in range(len(rank_sequence) - 4):
            if all(rank_sequence[i].value - 1 == rank_sequence[i + 1].value for
                   i in range(start_index, start_index + 4)):
                is_straight = True
                straight_high_card = rank_sequence[start_index]
                break

        # 检查同花顺和皇家同花顺
        if is_flash and is_straight:
            for start_index in range(len(flush_cards) - 4):
                if all(flush_cards[i].rank.value - 1 == flush_cards[i + 1].rank.value for i in
                       range(start_index, start_index + 4)):
                    if flush_cards[start_index].rank == Rank.A:
                        return (HandRanking(HandRank.ROYAL_FLUSH, flush_cards[start_index:start_index + 5]),
                                flush_cards[start_index:start_index + 5])
                    return (HandRanking(HandRank.STRAIGHT_FLUSH, flush_cards[start_index:start_index + 5]),
                            flush_cards[start_index:start_index + 5])

        # 四条
        for rank, count in rank_counts.items():
            if count == 4:
                four_cards = [card for card in sorted_cards if card.rank == rank]
                kicker_card = [card for card in sorted_cards if card.rank != rank][0]
                return HandRanking(HandRank.FOUR_OF_A_KIND, four_cards + [kicker_card]), four_cards + [kicker_card]

        # 葫芦
        three_card_rank = None
        pair_card_rank = None
        for rank, count in rank_counts.items():
            if count == 3:
                three_card_rank = rank
            elif count == 2:
                pair_card_rank = rank

        if three_card_rank and pair_card_rank:
            three_cards = [card for card in sorted_cards if card.rank == three_card_rank][:3]
            pair_cards = [card for card in sorted_cards if card.rank == pair_card_rank][:2]
            return HandRanking(HandRank.FULL_HOUSE, three_cards + pair_cards), three_cards + pair_cards

        # 同花
        if is_flash:
            sorted_flush_cards = sorted(flush_cards, key=lambda card: card.rank.value, reverse=True)
            return HandRanking(HandRank.FLUSH, sorted_flush_cards[:5]), sorted_flush_cards[:5]

        # 顺子
        if is_straight:
            straight_cards = []
            current_value = straight_high_card.value
            for card in sorted_cards:
                if card.rank.value == current_value:
                    straight_cards.append(card)
                    if len(straight_cards) == 5:
                        break
                    current_value -= 1
            return HandRanking(HandRank.STRAIGHT, [card.rank for card in straight_cards]), straight_cards

        # 三条
        if three_card_rank:
            three_cards = [card for card in sorted_cards if card.rank == three_card_rank][:3]
            kickers = [card for card in sorted_cards if card.rank != three_card_rank][:2]
            return HandRanking(HandRank.THREE_OF_A_KIND, three_cards + kickers), three_cards + kickers

        # 两对
        pairs = []
        kicker = None
        for rank, count in rank_counts.items():
            if count == 2:
                if len(pairs) < 4:
                    # 只添加当前找到的对，直到有两对
                    pairs.extend([card for card in sorted_cards if card.rank == rank])
            elif len(pairs) == 4:  # 确保已经找到两对再开始找kicker
                # 找到除了这两对之外的最高的牌作为kicker
                potential_kickers = [card for card in sorted_cards if card.rank not in [pair.rank for pair in pairs]]
                if potential_kickers:
                    kicker = potential_kickers[0]
                    break

        if len(pairs) == 4 and kicker:
            # 如果找到了两对并且有kicker
            return HandRanking(HandRank.TWO_PAIR, pairs + [kicker]), pairs + [kicker]

        # 一对
        if len(pairs) == 2:
            kickers = [card for card in sorted_cards if card.rank != pairs[0].rank][:3]
            return HandRanking(HandRank.ONE_PAIR, pairs + kickers), pairs + kickers

        # 高牌
        return HandRanking(HandRank.HIGH_CARD, sorted_cards[:5]), sorted_cards[:5]

    def get_hand_rank(self, cards: List[PokerCard]) -> HandRanking:
        """给定一组牌(五张)，返回 HandRanking 对象，表示这组牌的牌型和高牌"""

        return DefaultHandRankingEvaluateStrategy().get_hand_rank(cards)
