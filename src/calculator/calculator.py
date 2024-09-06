import copy
import itertools

from src.game.comparator.hand_comparator import GameResult, compare_two_players
from src.game.evaluator.hand_ranking_evaluate import HandEvaluator
from src.game.evaluator.strategy.better_strategy import BetterHandRankingEvaluateStrategy
from src.game.player import Player
from src.poker.deck import PokerDeck


class Calculator:
    @staticmethod
    def calc_win_prop_in_two_player(player1: Player, player2: Player, deck: PokerDeck = PokerDeck(is_complete=True)):
        """计算两位玩家之间的胜率, 在没有发公共牌的情况下"""
        wins = 0
        trials = 0
        local_deck = copy.deepcopy(deck)

        evaluator = HandEvaluator(BetterHandRankingEvaluateStrategy())

        # 1. 确定牌堆中没有两位玩家的手牌
        all_player_cards = player1.show_hand() + player2.show_hand()
        for card in all_player_cards:
            local_deck.remove_card(card=card)

        # 2. 循环遍历，从剩下的牌组中遍历所有可能的五张牌的情况
        for community_combo in itertools.combinations(local_deck, 5):
            trials += 1

            # 比较两位玩家的最佳手牌
            win: GameResult = compare_two_players(player1, player2, list(community_combo), evaluator)
            print(
                f"{trials} "
                f"Community combo: {' '.join(card.display() for card in community_combo)}"
                f" Player1-Win: {win.name}"
            )
            if win == GameResult.WIN:
                wins += 1
            elif win == GameResult.TIE:
                wins += 0.5

        # 3. 计算并返回胜率
        win_probability = wins / trials if trials > 0 else 0
        print("Player1 wins prop: ", win_probability)
        return win_probability
