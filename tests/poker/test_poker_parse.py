import pytest

from src.poker.poker import PokerCard, Rank, Suit


# 参数化测试正确解析的案例
@pytest.mark.parametrize(
    "card_str, expected_suit, expected_rank",
    [
        ("H2", Suit.HEARTS, Rank.TWO),
        ("H10", Suit.HEARTS, Rank.TEN),
        ("D2", Suit.DIAMONDS, Rank.TWO),
        ("CQ", Suit.CLUBS, Rank.Q),
        ("SK", Suit.SPADES, Rank.K),
        ("♥A", Suit.HEARTS, Rank.A),
        ("♦J", Suit.DIAMONDS, Rank.J),
        ("♣7", Suit.CLUBS, Rank.SEVEN),
        ("♠9", Suit.SPADES, Rank.NINE),
    ]
)
def test_parse_valid(card_str, expected_suit, expected_rank):
    card = PokerCard.parse(card_str)
    assert card.suit == expected_suit
    assert card.rank == expected_rank


# 参数化测试无效输入的案例
@pytest.mark.parametrize(
    "invalid_card_str",
    [
        "Z2",  # 无效的花色
        "H1",  # 无效的牌面
        "D123",  # 不存在的牌面
        "C$",  # 非法字符
        "S10K",  # 多余字符
        "",  # 空字符串
    ]
)
def test_parse_invalid(invalid_card_str):
    with pytest.raises(ValueError):
        PokerCard.parse(invalid_card_str)
