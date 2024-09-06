import copy
import itertools
import multiprocessing
from functools import partial

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
        print("Total trails: ", trials)
        print("Wins sum: ", wins)
        print("Player1 wins prop: ", win_probability)
        return win_probability

    @staticmethod
    def calc_win_prop_in_two_player_multi_process(
            player1: Player,
            player2: Player,
            deck: PokerDeck = PokerDeck(is_complete=True),
            process_num: int = 4
    ):
        """计算两位玩家之间的胜率, 在没有发公共牌的情况下, 使用多进程的方法加速"""
        local_deck = copy.deepcopy(deck)
        evaluator = HandEvaluator(BetterHandRankingEvaluateStrategy())

        # 确定牌堆中没有两位玩家的手牌
        all_player_cards = player1.show_hand() + player2.show_hand()
        for card in all_player_cards:
            local_deck.remove_card(card=card)

        # 使用进程池处理所有的社区牌组合x
        pool = multiprocessing.Pool(process_num)
        trials = list(itertools.combinations(local_deck, 5))

        # 使用偏函数来绑定静态参数，确保正确传递 player1, player2 和 evaluator
        worker_func = partial(_compare_players, player1=player1, player2=player2, evaluator=evaluator)

        results = pool.map(worker_func, trials)
        pool.close()
        pool.join()

        # 计算总的胜率
        wins = sum(result[0] for result in results)
        total_trials = sum(result[1] for result in results)
        win_probability = wins / total_trials if total_trials > 0 else 0
        print("Total trails: ", total_trials)
        print("Wins sum: ", wins)
        print("Player1 wins prop: ", win_probability)
        return win_probability


def _compare_players(community_combo, player1, player2, evaluator):
    """用于比较两位玩家并返回结果的辅助函数"""

    win = compare_two_players(player1, player2, list(community_combo), evaluator)
    print(
        f"Community combo: {' '.join(card.display() for card in community_combo)}"
        f" Player1-Win: {win.name}"
    )
    win_count = 1 if win == GameResult.WIN else 0.5 if win == GameResult.TIE else 0
    return win_count, 1
