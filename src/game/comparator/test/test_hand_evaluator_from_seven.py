import unittest

from src.game.comparator.hand_rank import HandRank
from src.game.comparator.hand_ranking_evaluate import (
    DefaultHandRankingEvaluateStrategy, HandEvaluator)
from src.poker.poker import PokerCard, Rank, Suit


class TestGetBestHandFromSeven(unittest.TestCase):
    def setUp(self):
        """在每个测试方法执行前初始化 HandEvaluator"""
        self.hand_evaluator = HandEvaluator(DefaultHandRankingEvaluateStrategy())

    def test_royal_flush(self):
        """测试七张牌中有皇家同花顺的情况"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.HEARTS, Rank.K),
            PokerCard(Suit.HEARTS, Rank.Q),
            PokerCard(Suit.HEARTS, Rank.J),
            PokerCard(Suit.HEARTS, Rank.TEN),
            PokerCard(Suit.CLUBS, Rank.TWO),
            PokerCard(Suit.DIAMONDS, Rank.THREE)
        ]
        best_hand, best_combination = self.hand_evaluator.get_best_hand_from_seven(cards)
        self.assertEqual(best_hand.rank, HandRank.ROYAL_FLUSH)
        self.assertEqual(best_combination, [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.HEARTS, Rank.K),
            PokerCard(Suit.HEARTS, Rank.Q),
            PokerCard(Suit.HEARTS, Rank.J),
            PokerCard(Suit.HEARTS, Rank.TEN)
        ])

    def test_straight_flush(self):
        """测试七张牌中有同花顺的情况"""
        cards = [
            PokerCard(Suit.SPADES, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.EIGHT),
            PokerCard(Suit.SPADES, Rank.SEVEN),
            PokerCard(Suit.SPADES, Rank.SIX),
            PokerCard(Suit.SPADES, Rank.FIVE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.DIAMONDS, Rank.THREE)
        ]
        best_hand, best_combination = self.hand_evaluator.get_best_hand_from_seven(cards)
        self.assertEqual(best_hand.rank, HandRank.STRAIGHT_FLUSH)
        self.assertEqual(best_combination, [
            PokerCard(Suit.SPADES, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.EIGHT),
            PokerCard(Suit.SPADES, Rank.SEVEN),
            PokerCard(Suit.SPADES, Rank.SIX),
            PokerCard(Suit.SPADES, Rank.FIVE)
        ])

    def test_four_of_a_kind(self):
        """测试七张牌中有四条的情况"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.NINE),
            PokerCard(Suit.DIAMONDS, Rank.NINE),
            PokerCard(Suit.CLUBS, Rank.NINE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.FOUR)
        ]
        best_hand, best_combination = self.hand_evaluator.get_best_hand_from_seven(cards)
        self.assertEqual(best_hand.rank, HandRank.FOUR_OF_A_KIND)
        self.assertEqual(best_combination, [
            PokerCard(Suit.HEARTS, Rank.NINE),
            PokerCard(Suit.DIAMONDS, Rank.NINE),
            PokerCard(Suit.CLUBS, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.NINE),
            PokerCard(Suit.DIAMONDS, Rank.FOUR)
        ])

    def test_full_house(self):
        """测试七张牌中有葫芦的情况"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.SPADES, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.SPADES, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.FOUR),
            PokerCard(Suit.DIAMONDS, Rank.FIVE)
        ]
        best_hand, best_combination = self.hand_evaluator.get_best_hand_from_seven(cards)
        self.assertEqual(best_hand.rank, HandRank.FULL_HOUSE)
        self.assertEqual(best_combination, [
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.THREE),
            PokerCard(Suit.SPADES, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.SPADES, Rank.TWO)
        ])

    def test_flush(self):
        """测试七张牌中有同花的情况"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.HEARTS, Rank.TEN),
            PokerCard(Suit.HEARTS, Rank.SIX),
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q)
        ]
        best_hand, best_combination = self.hand_evaluator.get_best_hand_from_seven(cards)
        self.assertEqual(best_hand.rank, HandRank.FLUSH)
        self.assertEqual(best_combination, [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.HEARTS, Rank.TEN),
            PokerCard(Suit.HEARTS, Rank.SIX),
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO)
        ])

    def test_straight(self):
        """测试七张牌中有顺子的情况"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.EIGHT),
            PokerCard(Suit.CLUBS, Rank.SEVEN),
            PokerCard(Suit.DIAMONDS, Rank.SIX),
            PokerCard(Suit.HEARTS, Rank.FIVE),
            PokerCard(Suit.CLUBS, Rank.A),
            PokerCard(Suit.DIAMONDS, Rank.K)
        ]
        best_hand, best_combination = self.hand_evaluator.get_best_hand_from_seven(cards)
        self.assertEqual(best_hand.rank, HandRank.STRAIGHT)
        self.assertEqual(best_combination, [
            PokerCard(Suit.HEARTS, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.EIGHT),
            PokerCard(Suit.CLUBS, Rank.SEVEN),
            PokerCard(Suit.DIAMONDS, Rank.SIX),
            PokerCard(Suit.HEARTS, Rank.FIVE)
        ])

    def test_three_of_a_kind(self):
        """测试七张牌中有三条的情况"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.FOUR),
            PokerCard(Suit.SPADES, Rank.FOUR),
            PokerCard(Suit.DIAMONDS, Rank.FOUR),
            PokerCard(Suit.CLUBS, Rank.SEVEN),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q)
        ]
        best_hand, best_combination = self.hand_evaluator.get_best_hand_from_seven(cards)
        self.assertEqual(best_hand.rank, HandRank.THREE_OF_A_KIND)
        self.assertEqual(best_combination, [
            PokerCard(Suit.HEARTS, Rank.FOUR),
            PokerCard(Suit.DIAMONDS, Rank.FOUR),
            PokerCard(Suit.SPADES, Rank.FOUR),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q)
        ])

    def test_two_pair(self):
        """测试七张牌中有两对的情况"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.SPADES, Rank.A),
            PokerCard(Suit.HEARTS, Rank.K),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.FOUR)
        ]
        best_hand, best_combination = self.hand_evaluator.get_best_hand_from_seven(cards)
        self.assertEqual(best_hand.rank, HandRank.TWO_PAIR)
        self.assertEqual(best_combination, [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.SPADES, Rank.A),
            PokerCard(Suit.HEARTS, Rank.K),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.FOUR)
        ])

    def test_one_pair(self):
        """测试七张牌中有一对的情况"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.J),
            PokerCard(Suit.SPADES, Rank.J),
            PokerCard(Suit.CLUBS, Rank.NINE),
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q)
        ]
        best_hand, best_combination = self.hand_evaluator.get_best_hand_from_seven(cards)
        self.assertEqual(best_hand.rank, HandRank.ONE_PAIR)
        self.assertEqual(best_combination, [
            PokerCard(Suit.HEARTS, Rank.J),
            PokerCard(Suit.SPADES, Rank.J),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q),
            PokerCard(Suit.CLUBS, Rank.NINE)
        ])

    def test_high_card(self):
        """测试七张牌中高牌的情况"""
        cards = [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.CLUBS, Rank.TEN),
            PokerCard(Suit.SPADES, Rank.SIX),
            PokerCard(Suit.DIAMONDS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q)
        ]
        best_hand, best_combination = self.hand_evaluator.get_best_hand_from_seven(cards)
        self.assertEqual(best_hand.rank, HandRank.HIGH_CARD)
        self.assertEqual(best_combination, [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q),
            PokerCard(Suit.CLUBS, Rank.TEN),
            PokerCard(Suit.SPADES, Rank.SIX)
        ])

if __name__ == '__main__':
    unittest.main()
