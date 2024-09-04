import pytest

from src.game.evaluator.hand_rank import HandRank
from src.game.evaluator.hand_ranking import HandRanking
from src.poker import Rank

test_data = [
    # 不同牌型比较：同花顺 > 顺子
    (HandRank.STRAIGHT_FLUSH, [Rank.A, Rank.K, Rank.Q, Rank.J, Rank.TEN], HandRank.STRAIGHT,
     [Rank.A, Rank.K, Rank.Q, Rank.J, Rank.TEN], "greater"),

    # 相同牌型，不同高牌：两个顺子，一个以Ace高，另一个以King高
    (HandRank.STRAIGHT, [Rank.A, Rank.K, Rank.Q, Rank.J, Rank.TEN], HandRank.STRAIGHT,
     [Rank.K, Rank.Q, Rank.J, Rank.TEN, Rank.NINE], "greater"),

    # 完全相同的手牌：同样的顺子，Ace高
    (HandRank.STRAIGHT, [Rank.A, Rank.K, Rank.Q, Rank.J, Rank.TEN], HandRank.STRAIGHT,
     [Rank.A, Rank.K, Rank.Q, Rank.J, Rank.TEN], "equal"),

    # 相同牌型，低牌比高牌：两个顺子，King高的低于Ace高的
    (HandRank.STRAIGHT, [Rank.K, Rank.Q, Rank.J, Rank.TEN, Rank.NINE], HandRank.STRAIGHT,
     [Rank.A, Rank.K, Rank.Q, Rank.J, Rank.TEN], "less"),
]


@pytest.mark.parametrize(
    "hand1_rank, hand1_high_cards, hand2_rank, hand2_high_cards, expected_result",
    test_data
)
def test_hand_ranking_comparison(hand1_rank, hand1_high_cards, hand2_rank, hand2_high_cards, expected_result):
    hand1 = HandRanking(hand1_rank, hand1_high_cards)
    hand2 = HandRanking(hand2_rank, hand2_high_cards)

    if expected_result == "greater":
        assert hand1 > hand2
    elif expected_result == "less":
        assert hand1 < hand2
    elif expected_result == "equal":
        assert hand1 == hand2
