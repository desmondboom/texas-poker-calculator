import pytest

from src.game.evaluator.hand_rank import HandRank
from src.game.evaluator.hand_ranking_evaluate import (
    HandEvaluator)
from src.poker.poker import PokerCard, Rank, Suit
from tests.game.evaluator.commons import error_message_with_strategy, get_strategies

# 测试数据：每个元素是一个包含描述、七张牌、预期最佳牌型和预期最佳五张牌的元组
test_data = [
    (
        "皇家同花顺",
        [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.HEARTS, Rank.K),
            PokerCard(Suit.HEARTS, Rank.Q),
            PokerCard(Suit.HEARTS, Rank.J),
            PokerCard(Suit.HEARTS, Rank.TEN),
            PokerCard(Suit.CLUBS, Rank.TWO),
            PokerCard(Suit.DIAMONDS, Rank.THREE)
        ],
        HandRank.ROYAL_FLUSH,
        [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.HEARTS, Rank.K),
            PokerCard(Suit.HEARTS, Rank.Q),
            PokerCard(Suit.HEARTS, Rank.J),
            PokerCard(Suit.HEARTS, Rank.TEN)
        ]
    ),
    (
        "同花顺",
        [
            PokerCard(Suit.SPADES, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.EIGHT),
            PokerCard(Suit.SPADES, Rank.SEVEN),
            PokerCard(Suit.SPADES, Rank.SIX),
            PokerCard(Suit.SPADES, Rank.FIVE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.DIAMONDS, Rank.THREE)
        ],
        HandRank.STRAIGHT_FLUSH,
        [
            PokerCard(Suit.SPADES, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.EIGHT),
            PokerCard(Suit.SPADES, Rank.SEVEN),
            PokerCard(Suit.SPADES, Rank.SIX),
            PokerCard(Suit.SPADES, Rank.FIVE)
        ]
    ),
    (
        "四条",
        [
            PokerCard(Suit.HEARTS, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.NINE),
            PokerCard(Suit.DIAMONDS, Rank.NINE),
            PokerCard(Suit.CLUBS, Rank.NINE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.FOUR)
        ],
        HandRank.FOUR_OF_A_KIND,
        [
            PokerCard(Suit.HEARTS, Rank.NINE),
            PokerCard(Suit.DIAMONDS, Rank.NINE),
            PokerCard(Suit.CLUBS, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.NINE),
            PokerCard(Suit.DIAMONDS, Rank.FOUR)
        ]
    ),
    (
        "葫芦",
        [
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.SPADES, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.SPADES, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.FOUR),
            PokerCard(Suit.DIAMONDS, Rank.FIVE)
        ],
        HandRank.FULL_HOUSE,
        [
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.THREE),
            PokerCard(Suit.SPADES, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.SPADES, Rank.TWO)
        ]
    ),
    (
        "同花",
        [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.HEARTS, Rank.TEN),
            PokerCard(Suit.HEARTS, Rank.SIX),
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q)
        ],
        HandRank.FLUSH,
        [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.HEARTS, Rank.TEN),
            PokerCard(Suit.HEARTS, Rank.SIX),
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO)
        ]
    ),
    (
        "顺子",
        [
            PokerCard(Suit.HEARTS, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.EIGHT),
            PokerCard(Suit.CLUBS, Rank.SEVEN),
            PokerCard(Suit.DIAMONDS, Rank.SIX),
            PokerCard(Suit.HEARTS, Rank.FIVE),
            PokerCard(Suit.CLUBS, Rank.A),
            PokerCard(Suit.DIAMONDS, Rank.K)
        ],
        HandRank.STRAIGHT,
        [
            PokerCard(Suit.HEARTS, Rank.NINE),
            PokerCard(Suit.SPADES, Rank.EIGHT),
            PokerCard(Suit.CLUBS, Rank.SEVEN),
            PokerCard(Suit.DIAMONDS, Rank.SIX),
            PokerCard(Suit.HEARTS, Rank.FIVE)
        ]
    ),
    (
        "三条",
        [
            PokerCard(Suit.HEARTS, Rank.FOUR),
            PokerCard(Suit.SPADES, Rank.FOUR),
            PokerCard(Suit.DIAMONDS, Rank.FOUR),
            PokerCard(Suit.CLUBS, Rank.SEVEN),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q)
        ],
        HandRank.THREE_OF_A_KIND,
        [
            PokerCard(Suit.HEARTS, Rank.FOUR),
            PokerCard(Suit.DIAMONDS, Rank.FOUR),
            PokerCard(Suit.SPADES, Rank.FOUR),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q)
        ]
    ),
    (
        "两对",
        [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.SPADES, Rank.A),
            PokerCard(Suit.HEARTS, Rank.K),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.FOUR)
        ],
        HandRank.TWO_PAIR,
        [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.SPADES, Rank.A),
            PokerCard(Suit.HEARTS, Rank.K),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.FOUR)
        ]
    ),
    (
        "一对",
        [
            PokerCard(Suit.HEARTS, Rank.J),
            PokerCard(Suit.SPADES, Rank.J),
            PokerCard(Suit.CLUBS, Rank.NINE),
            PokerCard(Suit.HEARTS, Rank.THREE),
            PokerCard(Suit.DIAMONDS, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q)
        ],
        HandRank.ONE_PAIR,
        [
            PokerCard(Suit.HEARTS, Rank.J),
            PokerCard(Suit.SPADES, Rank.J),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q),
            PokerCard(Suit.CLUBS, Rank.NINE)
        ]
    ),
    (
        "高牌",
        [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.CLUBS, Rank.TEN),
            PokerCard(Suit.SPADES, Rank.SIX),
            PokerCard(Suit.DIAMONDS, Rank.THREE),
            PokerCard(Suit.HEARTS, Rank.TWO),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q)
        ],
        HandRank.HIGH_CARD,
        [
            PokerCard(Suit.HEARTS, Rank.A),
            PokerCard(Suit.CLUBS, Rank.K),
            PokerCard(Suit.DIAMONDS, Rank.Q),
            PokerCard(Suit.CLUBS, Rank.TEN),
            PokerCard(Suit.SPADES, Rank.SIX)
        ]
    )
]


@pytest.mark.parametrize("strategy", get_strategies())
@pytest.mark.parametrize("description, cards, expected_rank, expected_combination", test_data)
def test_get_best_hand_from_seven(strategy, description, cards, expected_rank, expected_combination):
    """测试七张牌中选出最好的五张牌，覆盖不同策略"""
    hand_evaluator = HandEvaluator(strategy)
    best_hand, best_combination = hand_evaluator.get_best_hand_from_seven(cards)

    assert best_hand.ranking == expected_rank, error_message_with_strategy(description, strategy)
    assert best_combination == expected_combination, error_message_with_strategy(description, strategy)


if __name__ == "__main__":
    pytest.main()
