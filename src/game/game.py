from typing import List

from src.game.player import Player
from src.poker import PokerCard, PokerDeck


class Game:
    def __init__(self, players: List[Player]) -> None:
        self.deck = PokerDeck(is_complete=True)  # 创建一个完整的扑克牌堆
        self.players = players  # 绑定玩家
        self.community_cards: List[PokerCard] = []

        # 洗牌
        self.deck.shuffle()

    def start_game(self) -> None:
        """为每位玩家发两张底牌"""
        for player in self.players:
            for _ in range(2):  # 每位玩家发两张底牌
                card = self.deck.draw_cards(1)[0]
                player.draw_card(card)

    def flop(self) -> None:
        """翻牌：展示三张公共牌"""
        self.community_cards.extend(self.deck.draw_cards(3))

    def turn(self) -> None:
        """转牌：展示第四张公共牌"""
        self.community_cards.append(self.deck.draw_cards(1)[0])

    def river(self) -> None:
        """河牌：展示第五张公共牌"""
        self.community_cards.append(self.deck.draw_cards(1)[0])

    def show_community_cards(self) -> List[PokerCard]:
        """返回公共牌"""
        return self.community_cards

    def show_players_hands(self) -> None:
        """显示每位玩家的手牌"""
        for player in self.players:
            print(f"{player.name}'s hand: {player.show_hand()}")


# 使用示例
if __name__ == "__main__":
    # 创建玩家
    player1 = Player("Alice")
    player2 = Player("Bob")

    # 创建游戏并开始
    game = Game([player1, player2])
    game.start_game()

    # 显示玩家的底牌
    game.show_players_hands()

    # 进行翻牌、转牌、河牌
    game.flop()
    print("Flop:", game.show_community_cards())

    game.turn()
    print("Turn:", game.show_community_cards())

    game.river()
    print("River:", game.show_community_cards())
