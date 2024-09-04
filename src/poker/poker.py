from . import Rank, Suit


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

    def __str__(self) -> str:
        return self.display()

    @staticmethod
    def parse(card_str: str) -> 'PokerCard':
        if not card_str:
            raise ValueError("Input string cannot be empty.")

        suit_map = {
            'H': Suit.HEARTS, 'D': Suit.DIAMONDS, 'C': Suit.CLUBS, 'S': Suit.SPADES,
            '♥': Suit.HEARTS, '♦': Suit.DIAMONDS, '♣': Suit.CLUBS, '♠': Suit.SPADES
        }
        suit_char = card_str[0]
        suit = suit_map.get(suit_char)

        if suit is None:
            raise ValueError(f"Invalid suit symbol: {suit_char}")

        rank_str = card_str[1:]
        try:
            rank = Rank.from_string(rank_str)
        except KeyError:
            raise ValueError(f"Invalid rank symbol: {rank_str}")

        return PokerCard(suit, rank)
