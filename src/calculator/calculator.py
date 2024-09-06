import copy
import itertools
import multiprocessing
import random
from functools import partial

from src.game.comparator.hand_comparator import GameResult, compare_two_players
from src.game.evaluator.hand_ranking_evaluate import HandEvaluator
from src.game.evaluator.strategy.better_strategy import BetterHandRankingEvaluateStrategy
from src.game.player import Player
from src.poker.deck import PokerDeck


class Calculator:
    def __init__(self, evaluator: HandEvaluator = HandEvaluator(BetterHandRankingEvaluateStrategy())):
        self.evaluator = evaluator

    @staticmethod
    def remove_player_cards(deck, player1, player2):
        """从牌组中移除两位玩家的手牌"""
        local_deck = copy.deepcopy(deck)
        all_player_cards = player1.show_hand() + player2.show_hand()
        for card in all_player_cards:
            local_deck.remove_card(card=card)
        return local_deck

    def calc_win_prop_in_two_player(
            self,
            player1: Player,
            player2: Player,
            deck: PokerDeck = PokerDeck(is_complete=True)
    ):
        """计算两位玩家之间的胜率, 在没有发公共牌的情况下"""
        wins = 0
        trials = 0
        local_deck = self.remove_player_cards(deck, player1, player2)

        # 循环遍历，从剩下的牌组中遍历所有可能的五张牌的情况
        for community_combo in itertools.combinations(local_deck, 5):
            trials += 1

            # 比较两位玩家的最佳手牌
            win: GameResult = compare_two_players(player1, player2, list(community_combo), self.evaluator)
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
        print("Player1 wins prop: ", f'{win_probability:.2%}')
        return win_probability

    def calc_win_prop_in_two_player_multi_process(
            self,
            player1: Player,
            player2: Player,
            deck: PokerDeck = PokerDeck(is_complete=True),
            process_num: int = 4
    ):
        """计算两位玩家之间的胜率, 在没有发公共牌的情况下, 使用多进程的方法加速"""
        local_deck = self.remove_player_cards(deck, player1, player2)

        # 使用进程池处理所有的社区牌组合x
        pool = multiprocessing.Pool(process_num)
        trials = list(itertools.combinations(local_deck, 5))

        # 使用偏函数来绑定静态参数，确保正确传递 player1, player2 和 evaluator
        worker_func = partial(self._compare_players, player1=player1, player2=player2)

        results = pool.map(worker_func, trials)
        pool.close()
        pool.join()

        # 计算总的胜率
        wins = sum(result[0] for result in results)
        total_trials = sum(result[1] for result in results)
        win_probability = wins / total_trials if total_trials > 0 else 0
        print("Total trails: ", total_trials)
        print("Wins sum: ", wins)
        print("Player1 wins prop: ", f'{win_probability:.2%}')
        return win_probability

    def calc_win_prop_monte_carlo(
            self,
            player1: Player,
            player2: Player,
            deck: PokerDeck = PokerDeck(is_complete=True),
            num_simulations: int = 100_000,
            process_num: int = 4
    ):
        """计算两位玩家之间的胜率, 使用蒙特卡洛模拟来加速计算"""
        local_deck = self.remove_player_cards(deck, player1, player2)
        all_combinations = list(itertools.combinations(local_deck, 5))

        print("开始蒙特卡洛模拟，样本量为", num_simulations)
        # 随机选择指定数量的社区牌组合进行模拟
        trials = random.sample(all_combinations, min(num_simulations, len(all_combinations)))

        # 使用进程池处理所选的社区牌组合
        with multiprocessing.Pool(process_num) as pool:
            worker_func = partial(self._compare_players, player1=player1, player2=player2)
            results = pool.map(worker_func, trials)

        # 计算总的胜率
        wins = sum(result[0] for result in results)
        total_trials = len(trials)
        win_probability = wins / total_trials if total_trials > 0 else 0
        print("蒙特卡洛样本数 Total trials: ", total_trials)
        print("Wins sum: ", wins)
        print("Player1 wins prop: ", f'{win_probability:.2%}')
        return win_probability

    def monte_carlo_simulate_win_probability(
            self,
            player1: Player,
            player2: Player,
            deck: PokerDeck = PokerDeck(is_complete=True),
            num_simulations: int = 100_000
    ):
        """使用蒙特卡洛模拟来估计玩家1的胜率, 打印出拟合图像来展示拟合状态"""
        # TODO: 打印图像
        local_deck = self.remove_player_cards(deck, player1, player2)
        all_combinations = list(itertools.combinations(local_deck, 5))
        wins = 0
        trials = 0

        print("开始蒙特卡洛模拟，样本量为", num_simulations)
        for _ in range(num_simulations):
            community_combo = random.choice(all_combinations)
            win = compare_two_players(player1, player2, list(community_combo), self.evaluator)
            wins += 1 if win == GameResult.WIN else 0.5 if win == GameResult.TIE else 0
            trials += 1
            win_probability = wins / trials

            if trials % 100 == 0:
                print(f"After {trials} trials, current Player1 win probability: {win_probability:.4f}")

        print("Final win probability:", f"{win_probability:.4f}")
        return win_probability

    def _compare_players(self, community_combo, player1, player2):
        """用于比较两位玩家并返回结果的辅助函数"""
        evaluator = self.evaluator
        win = compare_two_players(player1, player2, list(community_combo), evaluator)
        print(
            f"Community combo: {' '.join(card.display() for card in community_combo)}"
            f" Player1-Win: {win.name}"
        )
        win_count = 1 if win == GameResult.WIN else 0.5 if win == GameResult.TIE else 0
        return win_count, 1
