from enum import Enum


class Suit(Enum):
    HEARTS = ('Hearts', '♥')
    DIAMONDS = ('Diamonds', '♦')
    CLUBS = ('Clubs', '♣')
    SPADES = ('Spades', '♠')

    def __init__(self, label: str, symbol: str):
        self.label = label
        self.symbol = symbol

class Rank(Enum):
    A = (14, 'A')
    K = (13, 'K')
    Q = (12, 'Q')
    J = (11, 'J')
    TEN = (10, '10')
    NINE = (9, '9')
    EIGHT = (8, '8')
    SEVEN = (7, '7')
    SIX = (6, '6')
    FIVE = (5, '5')
    FOUR = (4, '4')
    THREE = (3, '3')
    TWO = (2, '2')

    def __init__(self, value: int, display: str):
        self._value_ = value  # 设置枚举的内部值
        self.display = display  # 可供展示的字符串

    def display(self):
        return self.display

class PokerCard:
    def __init__(self, suit: Suit, rank: Rank) -> None:
        self.suit: Suit = suit
        self.rank: Rank = rank
        
    def __eq__(self, other: object) -> bool:
        if isinstance(other, PokerCard):
            return self.suit == other.suit and self.rank == other.rank
        return False

    def __hash__(self) -> int:
        return hash((self.suit, self.rank))
        
    def display(self) -> str:
        return f"{self.suit.symbol}{self.rank.display}"

    @staticmethod
    def parse(card_str: str) -> 'PokerCard':
        # 扑克牌花色符号映射
        suit_map = {
            'H': Suit.HEARTS, 'D': Suit.DIAMONDS, 'C': Suit.CLUBS, 'S': Suit.SPADES,
            '♥': Suit.HEARTS, '♦': Suit.DIAMONDS, '♣': Suit.CLUBS, '♠': Suit.SPADES
        }

        # 解析花色字符
        suit_char = card_str[0]
        suit = suit_map.get(suit_char)

        # 检查是否为有效的花色符号
        if suit is None:
            raise ValueError(f"Invalid suit symbol: {suit_char}")

        # 剩下的部分是点数
        rank_str = card_str[1:].replace('10', 'TEN').upper()  # 处理 '10' 并转为大写
        rank = Rank[rank_str]  # 使用枚举名称查找

        return PokerCard(suit, rank)