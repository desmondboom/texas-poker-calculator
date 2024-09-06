import time

from src.calculator.calculator import Calculator
from src.game.player import Player
from src.poker.deck import PokerDeck
from src.poker.poker import PokerCard


def main():
    # 开始计时
    start_time = time.time()

    # 创建一副完整的扑克牌堆
    deck = PokerDeck(is_complete=True)

    # 创建两个玩家
    player1 = Player("Alice")
    player2 = Player("Bob")

    # 给玩家随机发两张手牌
    deck.shuffle()  # 确保发牌前牌堆是随机的
    player1.draw_card(PokerCard.parse("HA"))
    player1.draw_card(PokerCard.parse("DA"))
    player2.draw_card(PokerCard.parse("CA"))
    player2.draw_card(PokerCard.parse("SA"))

    # 输出玩家手牌
    print(f"Player 1: {player1.name} has {[card.display() for card in player1.show_hand()]}")
    print(f"Player 2: {player2.name} has {[card.display() for card in player2.show_hand()]}")

    win_prop_player1 = Calculator.calc_win_prop_in_two_player_multi_process(player1, player2)
    print(f"Player 1 win probability: {win_prop_player1:.2%}")

    # 结束计时并输出耗时
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"Time taken: {minutes}m{seconds}s")


if __name__ == "__main__":
    main()
