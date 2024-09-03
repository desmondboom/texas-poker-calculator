import copy
import itertools

from src.game.comparator.hand_ranking_evaluate import DefaultHandRankingEvaluateStrategy, HandEvaluator
from src.game.player import Player
from src.poker.deck import PokerDeck


class Evaluator:
    @staticmethod
    def calc_win_prop_in_two_player(player1: Player, player2: Player, deck: PokerDeck = PokerDeck(isComplete=True)):
        """计算两位玩家之间的胜率, 在没有发公共牌的情况下"""
        wins = 0
        trials = 0
        local_deck = copy.deepcopy(deck)
        
        evaluator = HandEvaluator(DefaultHandRankingEvaluateStrategy())
        
        # 1. 确定牌堆中没有两位玩家的手牌
        all_player_cards = player1.show_hand() + player2.show_hand()
        for card in all_player_cards:
            local_deck.remove_card(card=card)
        
        # 2. 循环遍历，从剩下的牌组中遍历所有可能的五张牌的情况
        for community_combo in itertools.combinations(local_deck, 5):
            trials += 1
            all_cards_player1 = player1.show_hand() + list(community_combo)
            all_cards_player2 = player2.show_hand() + list(community_combo)

            # 计算每位玩家的最佳五张牌
            best_hand_player1, _ = evaluator.get_best_hand_from_seven(all_cards_player1)
            best_hand_player2, _ = evaluator.get_best_hand_from_seven(all_cards_player2)
            
            # 比较两位玩家的最佳手牌
            win = best_hand_player1 >= best_hand_player2
            print(f"#{trials} Community combo: {' '.join(card.display() for card in community_combo)} Player1-Win: {win}")
            if win:
                wins += 1
            
            
        # 3. 计算并返回胜率
        win_probability = wins / trials if trials > 0 else 0
        print("Player1 wins prop: ", win_probability)
        return win_probability
