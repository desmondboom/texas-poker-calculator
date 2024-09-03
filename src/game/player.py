from typing import List

from src.poker import PokerCard


class Player:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.__hand: List[PokerCard] = []

    def draw_card(self, card: PokerCard) -> None:
        if len(self.__hand) < 2:
            self.__hand.append(card)

    def show_hand(self) -> List[PokerCard]:
        """返回玩家的手牌"""
        return self.__hand
