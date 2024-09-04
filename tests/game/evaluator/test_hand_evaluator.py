import pytest

from src.game.evaluator.hand_rank import HandRank
from src.game.evaluator.hand_ranking_evaluate import HandEvaluator
from src.poker.poker import PokerCard, Rank, Suit
from tests.game.evaluator.commons import error_message_with_strategy, get_strategies

# 测试数据：每个元素是一个包含测试牌型和预期HandRank的元组
test_data = [
    (
        "皇家同花顺",
        [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.HEARTS, Rank.K),
            PokerCard(Suit.HEARTS, Rank.Q),
            PokerCard(Suit.HEARTS, Rank.J),
            PokerCard(Suit.HEARTS, Rank.TEN)
        ],
        HandRank.ROYAL_FLUSH
    ),
    (
        "同花顺",
        [
            PokerCard(Suit.SPADES, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.EIGHT),
            PokerCard(Suit.SPADES, Rank.SEVEN),
            PokerCard(Suit.SPADES, Rank.SIX),
            PokerCard(Suit.SPADES, Rank.FIVE)
        ],
        HandRank.STRAIGHT_FLUSH
    ),
    (
        "四条",
        [
            PokerCard(Suit.HEARTS, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.NINE),
            PokerCard(Suit.DIAMONDS, Rank.NINE),
            PokerCard(Suit.CLUBS, Rank.NINE),
            PokerCard(Suit.HEARTS, Rank.TWO)
        ],
        HandRank.FOUR_OF_A_KIND
    ),
    (
        "满堂红（葫芦）",
        [
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.SPADES, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.SPADES, Rank.TWO)
        ],
        HandRank.FULL_HOUSE
    ),
    (
        "同花",
        [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.HEARTS, Rank.TEN),
            PokerCard(Suit.HEARTS, Rank.SIX),
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO)
        ],
        HandRank.FLUSH
    ),
    (
        "顺子",
        [
            PokerCard(Suit.HEARTS, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.EIGHT),
            PokerCard(Suit.CLUBS, Rank.SEVEN),
            PokerCard(Suit.DIAMONDS, Rank.SIX),
            PokerCard(Suit.HEARTS, Rank.FIVE)
        ],
        HandRank.STRAIGHT
    ),
    (
        "三条",
        [
            PokerCard(Suit.HEARTS, Rank.FOUR),
            PokerCard(Suit.SPADES, Rank.FOUR),
            PokerCard(Suit.DIAMONDS, Rank.FOUR),
            PokerCard(Suit.CLUBS, Rank.SEVEN),
            PokerCard(Suit.HEARTS, Rank.TWO)
        ],
        HandRank.THREE_OF_A_KIND
    ),
    (
        "两对",
        [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.SPADES, Rank.A),
            PokerCard(Suit.HEARTS, Rank.K),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.HEARTS, Rank.TWO)
        ],
        HandRank.TWO_PAIR
    ),
    (
        "一对",
        [
            PokerCard(Suit.HEARTS, Rank.J),
            PokerCard(Suit.SPADES, Rank.J),
            PokerCard(Suit.CLUBS, Rank.NINE),
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.TWO)
        ],
        HandRank.ONE_PAIR
    ),
    (
        "高牌",
        [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.CLUBS, Rank.TEN),
            PokerCard(Suit.SPADES, Rank.SIX),
            PokerCard(Suit.DIAMONDS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO)
        ],
        HandRank.HIGH_CARD
    )
]


@pytest.mark.parametrize("strategy", get_strategies())
@pytest.mark.parametrize("description, cards, expected_rank", test_data)
def test_get_hand_rank(strategy, description, cards, expected_rank):
    """测试不同策略下的牌型评估"""
    hand_evaluator = HandEvaluator(strategy)
    result = hand_evaluator.get_hand_rank(cards)
    assert result.rank == expected_rank, error_message_with_strategy(description, strategy)


if __name__ == "__main__":
    pytest.main()
