from collections import Counter
from typing import List, Tuple

from src.game.evaluator.hand_rank import HandRank
from src.game.evaluator.hand_ranking import HandRanking
from src.game.evaluator.strategy.strategy import HandRankingEvaluateStrategy
from src.game.evaluator.strategy.utils import get_hand_card_rank, sort_hand_card
from src.poker import PokerCard, Rank


class RuleHandRankingEvaluateStrategy(HandRankingEvaluateStrategy):
    """使用改进的策略从七张牌中确定最佳五张牌的牌型"""

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def categorize_by_suit_and_rank(cards: List[PokerCard]) -> Tuple[Counter, Counter]:
        """分类统计牌的花色和点数"""
        suits = Counter(card.suit for card in cards)
        ranks = Counter(card.rank for card in cards)
        return suits, ranks

    @staticmethod
    def find_flush(sorted_cards: List[PokerCard], suit_counts: Counter) -> List[PokerCard]:
        """查找同花，如果存在返回五张同花牌，否则返回空列表"""
        for suit, count in suit_counts.items():
            if count >= 5:
                return [card for card in sorted_cards if card.suit == suit][:5]
        return []

    @staticmethod
    def find_straight(sorted_cards: List[PokerCard]) -> List[PokerCard]:
        """查找顺子，如果存在返回五张顺子牌，否则返回空列表"""
        rank_sequence = sorted(set(card.rank for card in sorted_cards), reverse=True)
        for i in range(len(rank_sequence) - 4):
            if all(rank_sequence[j].value - 1 == rank_sequence[j + 1].value for j in range(i, i + 4)):
                return [card for card in sorted_cards if card.rank in rank_sequence[i:i + 5]]
        return []

    def check_royal_flush(self, flush_cards: List[PokerCard]) -> List[PokerCard]:
        """检查皇家同花顺，如果存在返回五张牌，否则返回空列表"""
        if flush_cards and flush_cards[0].rank == Rank.A:
            straight_flush = self.find_straight(flush_cards)
            if straight_flush and straight_flush[0].rank == Rank.A:
                return straight_flush
        return []

    @staticmethod
    def find_four_of_a_kind(sorted_cards: List[PokerCard], rank_counts: Counter) -> List[PokerCard]:
        """查找四条，如果存在返回四条牌加一张高牌，否则返回空列表"""
        for rank, count in rank_counts.items():
            if count == 4:
                four_cards = [card for card in sorted_cards if card.rank == rank]
                kicker = [card for card in sorted_cards if card.rank != rank][0]
                return four_cards + [kicker]
        return []

    @staticmethod
    def find_full_house(sorted_cards: List[PokerCard], rank_counts: Counter) -> List[PokerCard]:
        """查找葫芦（三条+对子），如果存在返回五张牌，否则返回空列表"""
        three_of_a_kind = []
        pair = []
        for rank, count in rank_counts.items():
            if count == 3 and not three_of_a_kind:
                three_of_a_kind = [card for card in sorted_cards if card.rank == rank][:3]
            elif count == 2 and not pair:
                pair = [card for card in sorted_cards if card.rank == rank][:2]
        if three_of_a_kind and pair:
            return three_of_a_kind + pair
        return []

    @staticmethod
    def find_three_of_a_kind(sorted_cards: List[PokerCard], rank_counts: Counter) -> List[PokerCard]:
        """查找三条，如果存在返回三张牌加两张高牌，否则返回空列表"""
        for rank, count in rank_counts.items():
            if count == 3:
                three_of_a_kind = [card for card in sorted_cards if card.rank == rank][:3]
                kickers = [card for card in sorted_cards if card.rank != rank][:2]
                return three_of_a_kind + kickers
        return []

    @staticmethod
    def find_two_pair(sorted_cards: List[PokerCard], rank_counts: Counter) -> List[PokerCard]:
        """查找两对，如果存在返回两对牌加一张高牌，否则返回空列表"""
        pairs = []
        for rank, count in rank_counts.items():
            if count == 2:
                pairs.extend([card for card in sorted_cards if card.rank == rank][:2])
        if len(pairs) >= 4:
            kicker = [card for card in sorted_cards if card.rank not in [p.rank for p in pairs]][0]
            return pairs[:4] + [kicker]
        return []

    @staticmethod
    def find_one_pair(sorted_cards: List[PokerCard], rank_counts: Counter) -> List[PokerCard]:
        """查找一对，如果存在返回一对牌加三张高牌，否则返回空列表"""
        for rank, count in rank_counts.items():
            if count == 2:
                pair = [card for card in sorted_cards if card.rank == rank][:2]
                kickers = [card for card in sorted_cards if card.rank != rank][:3]
                return pair + kickers
        return []

    @staticmethod
    def construct_hand_ranking(hand_rank: HandRank, cards: List[PokerCard]) -> Tuple[HandRanking, List[PokerCard]]:
        """构造并返回手牌的HandRanking对象及牌列表"""
        hand_ranking = get_hand_card_rank(cards)
        return HandRanking(hand_rank, hand_ranking), cards

    def get_best_hand_from_seven(self, cards: List[PokerCard]) -> Tuple[HandRanking, List[PokerCard]]:
        sorted_cards = sort_hand_card(cards)
        suit_counts, rank_counts = self.categorize_by_suit_and_rank(sorted_cards)

        # 检查皇家同花顺
        flush_cards = self.find_flush(sorted_cards, suit_counts)
        royal_flush_cards = self.check_royal_flush(flush_cards)
        if royal_flush_cards:
            return self.construct_hand_ranking(HandRank.ROYAL_FLUSH, royal_flush_cards)

        # 检查同花顺
        straight_flush_cards = self.find_straight(flush_cards)
        if straight_flush_cards:
            return self.construct_hand_ranking(HandRank.STRAIGHT_FLUSH, straight_flush_cards)

        # 检查四条
        four_of_a_kind_cards = self.find_four_of_a_kind(sorted_cards, rank_counts)
        if four_of_a_kind_cards:
            return self.construct_hand_ranking(HandRank.FOUR_OF_A_KIND, four_of_a_kind_cards)

        # 检查葫芦
        full_house_cards = self.find_full_house(sorted_cards, rank_counts)
        if full_house_cards:
            return self.construct_hand_ranking(HandRank.FULL_HOUSE, full_house_cards)

        # 检查同花
        if flush_cards:
            return self.construct_hand_ranking(HandRank.FLUSH, flush_cards)

        # 检查顺子
        straight_cards = self.find_straight(sorted_cards)
        if straight_cards:
            return self.construct_hand_ranking(HandRank.STRAIGHT, straight_cards)

        # 检查三条
        three_of_a_kind_cards = self.find_three_of_a_kind(sorted_cards, rank_counts)
        if three_of_a_kind_cards:
            return self.construct_hand_ranking(HandRank.THREE_OF_A_KIND, three_of_a_kind_cards)

        # 检查两对
        two_pair_cards = self.find_two_pair(sorted_cards, rank_counts)
        if two_pair_cards:
            return self.construct_hand_ranking(HandRank.TWO_PAIR, two_pair_cards)

        # 检查一对
        one_pair_cards = self.find_one_pair(sorted_cards, rank_counts)
        if one_pair_cards:
            return self.construct_hand_ranking(HandRank.ONE_PAIR, one_pair_cards)

        # 如果都没有，返回高牌
        high_card = sorted_cards[:5]
        return self.construct_hand_ranking(HandRank.HIGH_CARD, high_card)

    def get_hand_rank(self, cards: List[PokerCard]) -> HandRanking:
        """给定五张牌，返回HandRanking对象，表示这组牌的牌型"""
        ranking, _ = self.get_best_hand_from_seven(cards)
        return ranking
