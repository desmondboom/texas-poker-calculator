import random
from typing import List

from src.poker.poker import PokerCard, Rank, Suit


class PokerDeck:
    def __init__(self, isComplete: bool) -> None:
        self.__deck: List[PokerCard] = []
        if isComplete:
            self.__deck = [PokerCard(suit, rank) for suit in Suit for rank in Rank]
            
    def __iter__(self):
        return iter(self.__deck)
            
    def append_card(self, card: PokerCard) -> None:
        """将一张牌放入牌堆"""
        self.__deck.append(card)
        
    def append_cards(self, cards: List[PokerCard]) -> None:
        """将多张牌放入牌堆"""
        self.__deck.extend(cards)
        
    def remove_card(self, card: PokerCard) -> bool:
        """将一张牌从牌堆中移除"""
        if card in self.__deck:
            self.__deck.remove(card)
            return True
        else:
            return False
        
    def remove_cards(self, cards: List[PokerCard]) -> bool:
        """将多张牌从牌堆中移除，只有当所有牌都存在时才删除"""
        if all(card in self.__deck for card in cards):
            for card in cards:
                self.__deck.remove(card)
            return True
        else:
            return False

    def shuffle(self) -> None:
        """随机打乱牌组顺序"""
        random.shuffle(self.__deck)

    def draw_cards(self, n: int) -> List[PokerCard]:
        """按顺序取出n张牌, 返回包含取出的PokerCard对象的列表"""
        drawn_cards = []
        count = 0
        for card in self.__deck:
            drawn_cards.append(card)
            count += 1
            if count >= n:
                break
        return drawn_cards

    def reset_deck(self) -> None:
        """将所有的牌放回牌堆中"""
        self.in_deck = {card: True for card in self.deck}
        