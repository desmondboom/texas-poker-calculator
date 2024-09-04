import unittest

from src.game.evaluator.hand_rank import HandRank
from src.game.evaluator.hand_ranking_evaluate import (
    DefaultHandRankingEvaluateStrategy, HandEvaluator)
from src.poker.poker import PokerCard, Rank, Suit


class TestGetHandRank(unittest.TestCase):
    def setUp(self):
        """在每个测试方法执行前初始化 HandEvaluator"""
        self.hand_evaluator = HandEvaluator(DefaultHandRankingEvaluateStrategy())    

    def test_royal_flush(self):
        """测试皇家同花顺"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.HEARTS, Rank.K),
            PokerCard(Suit.HEARTS, Rank.Q),
            PokerCard(Suit.HEARTS, Rank.J),
            PokerCard(Suit.HEARTS, Rank.TEN)
        ]
        result = self.hand_evaluator.get_hand_rank(cards)
        self.assertEqual(result.rank, HandRank.ROYAL_FLUSH)

    def test_straight_flush(self):
        """测试同花顺"""
        cards = [
            PokerCard(Suit.SPADES, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.EIGHT),
            PokerCard(Suit.SPADES, Rank.SEVEN),
            PokerCard(Suit.SPADES, Rank.SIX),
            PokerCard(Suit.SPADES, Rank.FIVE)
        ]
        result = self.hand_evaluator.get_hand_rank(cards)
        self.assertEqual(result.rank, HandRank.STRAIGHT_FLUSH)

    def test_four_of_a_kind(self):
        """测试四条"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.NINE),
            PokerCard(Suit.DIAMONDS, Rank.NINE),
            PokerCard(Suit.CLUBS, Rank.NINE),
            PokerCard(Suit.HEARTS, Rank.TWO)
        ]
        result = self.hand_evaluator.get_hand_rank(cards)
        self.assertEqual(result.rank, HandRank.FOUR_OF_A_KIND)

    def test_full_house(self):
        """测试满堂红（葫芦）"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.SPADES, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.SPADES, Rank.TWO)
        ]
        result = self.hand_evaluator.get_hand_rank(cards)
        self.assertEqual(result.rank, HandRank.FULL_HOUSE)

    def test_flush(self):
        """测试同花"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.HEARTS, Rank.TEN),
            PokerCard(Suit.HEARTS, Rank.SIX),
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO)
        ]
        result = self.hand_evaluator.get_hand_rank(cards)
        self.assertEqual(result.rank, HandRank.FLUSH)

    def test_straight(self):
        """测试顺子"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.EIGHT),
            PokerCard(Suit.CLUBS, Rank.SEVEN),
            PokerCard(Suit.DIAMONDS, Rank.SIX),
            PokerCard(Suit.HEARTS, Rank.FIVE)
        ]
        result = self.hand_evaluator.get_hand_rank(cards)
        self.assertEqual(result.rank, HandRank.STRAIGHT)

    def test_three_of_a_kind(self):
        """测试三条"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.FOUR),
            PokerCard(Suit.SPADES, Rank.FOUR),
            PokerCard(Suit.DIAMONDS, Rank.FOUR),
            PokerCard(Suit.CLUBS, Rank.SEVEN),
            PokerCard(Suit.HEARTS, Rank.TWO)
        ]
        result = self.hand_evaluator.get_hand_rank(cards)
        self.assertEqual(result.rank, HandRank.THREE_OF_A_KIND)

    def test_two_pair(self):
        """测试两对"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.SPADES, Rank.A),
            PokerCard(Suit.HEARTS, Rank.K),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.HEARTS, Rank.TWO)
        ]
        result = self.hand_evaluator.get_hand_rank(cards)
        self.assertEqual(result.rank, HandRank.TWO_PAIR)

    def test_one_pair(self):
        """测试一对"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.J),
            PokerCard(Suit.SPADES, Rank.J),
            PokerCard(Suit.CLUBS, Rank.NINE),
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.TWO)
        ]
        result = self.hand_evaluator.get_hand_rank(cards)
        self.assertEqual(result.rank, HandRank.ONE_PAIR)

    def test_high_card(self):
        """测试高牌"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.CLUBS, Rank.TEN),
            PokerCard(Suit.SPADES, Rank.SIX),
            PokerCard(Suit.DIAMONDS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO)
        ]
        result = self.hand_evaluator.get_hand_rank(cards)
        self.assertEqual(result.rank, HandRank.HIGH_CARD)

if __name__ == '__main__':
    unittest.main()
