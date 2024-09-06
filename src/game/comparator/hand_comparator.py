from enum import Enum
from typing import List

from src.game.evaluator.hand_ranking import HandRanking
from src.game.evaluator.hand_ranking_evaluate import HandEvaluator
from src.game.evaluator.strategy.better_strategy import BetterHandRankingEvaluateStrategy
from src.game.player import Player
from src.poker.poker import PokerCard


class GameResult(Enum):
    WIN = 0
    LOSE = 1
    TIE = 2


def get_game_result(player1_rank: HandRanking, player2_rank: HandRanking) -> GameResult:
    if player1_rank > player2_rank:
        return GameResult.WIN
    elif player1_rank < player2_rank:
        return GameResult.LOSE
    else:
        return GameResult.TIE


def compare_two_players(
        player1: Player,
        player2: Player,
        community_cards: List[PokerCard],
        evaluator: HandEvaluator = HandEvaluator(BetterHandRankingEvaluateStrategy())
) -> GameResult:
    # 合并每位玩家的手牌和公共牌
    all_cards_player1 = player1.show_hand() + community_cards
    all_cards_player2 = player2.show_hand() + community_cards

    # 获取每位玩家的最佳五张牌的手牌排名
    best_hand_player1, _ = evaluator.get_best_hand_from_seven(all_cards_player1)
    best_hand_player2, _ = evaluator.get_best_hand_from_seven(all_cards_player2)

    # 比较两位玩家的最佳手牌
    return get_game_result(best_hand_player1, best_hand_player2)
