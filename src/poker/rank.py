from enum import Enum


class Rank(Enum):
    """扑克牌的点数"""
    A = 14
    K = 13
    Q = 12
    J = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2

    def __init__(self, value: int):
        self.display = self._generate_display(value)  # 可供展示的字符串

    @staticmethod
    def _generate_display(value):
        """根据数值生成显示用的字符串"""
        if 1 < value < 11:
            return str(value)
        elif value == 11:
            return 'J'
        elif value == 12:
            return 'Q'
        elif value == 13:
            return 'K'
        elif value == 14:
            return 'A'
        else:
            raise ValueError("无效的扑克牌点数")

    @classmethod
    def from_string(cls, s: str):
        """根据字符串返回相应的枚举成员"""
        for rank in cls:
            if rank.display == s.upper():
                return rank
        raise ValueError(f"无效的扑克牌点数: {s}")

    def __lt__(self, other):
        if isinstance(other, Rank):
            return self.value < other.value
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Rank):
            return self.value == other.value
        return NotImplemented

    def __hash__(self):
        return hash(self.value)

    def __deepcopy__(self, memo):
        return self
