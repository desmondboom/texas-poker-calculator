from enum import Enum


class Rank(Enum):
    """扑克牌的点数"""
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

    @classmethod
    def from_string(cls, s: str):
        """根据字符串返回相应的枚举成员"""
        for rank in cls:
            if rank.display == s.upper():
                return rank
        raise ValueError(f"无效的扑克牌点数: {s}")

    def __lt__(self, other):
        if isinstance(other, Rank):
            return self._value_ < other._value_
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Rank):
            return self._value_ == other._value_
        return NotImplemented

    def __hash__(self):
        return hash(self._value_)