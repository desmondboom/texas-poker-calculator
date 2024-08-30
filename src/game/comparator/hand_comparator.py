from enum import Enum
from typing import List

from .hand_evaluator import get_best_hand_from_seven
from ..player import Player
from ...poker.poker import PokerCard


class GameResult(Enum):
    WIN = 0
    LOSE = 1
    TIE = 2
    
def compare_two_players(player1: Player, player2: Player, community_cards: List[PokerCard]) -> GameResult:
    # 合并每位玩家的手牌和公共牌
    all_cards_player1 = player1.show_hand() + community_cards
    all_cards_player2 = player2.show_hand() + community_cards

    # 获取每位玩家的最佳五张牌的手牌排名
    best_hand_player1, _ = get_best_hand_from_seven(all_cards_player1)
    best_hand_player2, _ = get_best_hand_from_seven(all_cards_player2)

    # 比较两位玩家的最佳手牌
    if best_hand_player1 > best_hand_player2:
        return GameResult.WIN
    elif best_hand_player1 < best_hand_player2:
        return GameResult.LOSE
    else:
        return GameResult.TIE