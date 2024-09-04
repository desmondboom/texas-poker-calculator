import pytest

from src.poker import PokerCard
from src.game.player import Player
from src.game.comparator.hand_comparator import GameResult, compare_two_players

test_data = [
    # 高牌 vs 高牌
    (["HA", "H2"], ["CK", "D2"], ["H3", "S4", "D5", "C7", "D8"], GameResult.WIN),

    # 一对 vs 高牌
    (["HA", "DA"], ["CK", "DQ"], ["H2", "S3", "D4", "C5", "D8"], GameResult.WIN),

    # 两对 vs 一对，Pair of Aces and Twos vs Pair of Kings
    (["HA", "DA"], ["CQ", "DK"], ["H2", "D2", "S3", "H7", "D8"], GameResult.WIN),

    # 三条 vs 两对，Three Aces vs Pair of Kings and Queens
    (["HA", "DA"], ["CQ", "D3"], ["CA", "DQ", "H3", "H7", "D8"], GameResult.WIN),

    # 顺子 vs 三条，Straight 2 to 6 vs Three Kings
    (["H2", "D3"], ["CK", "DK"], ["C4", "S5", "H6", "DA", "HK"], GameResult.WIN),

    # 同花 vs 顺子，Flush in hearts vs Straight 7 to Jack
    (["H2", "H3"], ["D7", "D8"], ["H4", "H5", "H7", "D9", "D10"], GameResult.WIN),

    # 葫芦 vs 同花，Full House Aces over Kings vs Flush in diamonds
    (["HA", "DA"], ["D2", "D3"], ["CA", "CK", "DK", "D5", "D6"], GameResult.WIN),

    # 铁支 vs 葫芦，Four Aces vs Full House Kings over Queens
    (["HA", "DA"], ["CK", "DK"], ["CA", "SA", "HQ", "DQ", "HK"], GameResult.WIN),

    # 同花顺 vs 铁支，Straight Flush to the Ace vs Four Kings
    (["HA", "H10"], ["CK", "DK"], ["HJ", "HQ", "HK", "H9", "SK"], GameResult.WIN),

    # 皇家同花顺 vs 同花顺，Royal Flush in hearts vs Straight Flush to the King
    (["HA", "HK"], ["H9", "H8"], ["HQ", "HJ", "H10", "D2", "D3"], GameResult.WIN),
]


@pytest.mark.parametrize(
    "cards_player1, cards_player2, community_cards, expected_result",
    test_data
)
def test_compare_two_players(cards_player1, cards_player2, community_cards, expected_result):
    player1 = Player("Alice")
    player2 = Player("Bob")

    # 使用 PokerCard.parse 方法创建牌组
    for card_str in cards_player1:
        player1.draw_card(PokerCard.parse(card_str))
    for card_str in cards_player2:
        player2.draw_card(PokerCard.parse(card_str))
    community = [PokerCard.parse(card) for card in community_cards]
    
    result = compare_two_players(player1, player2, community)
    assert result == expected_result
