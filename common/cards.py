from __future__ import annotations

import random
import struct
from dataclasses import dataclass
from typing import List

SUITS = ["Heart", "Diamond", "Club", "Spade"]
RANKS = list(range(1, 14))

@dataclass(frozen=True)
class Card:
    rank: int
    suit: int

    def value(self) -> int:
        if self.rank == 1:
            return 11
        if self.rank >= 11:
            return 10
        return self.rank

    def encode3(self) -> bytes:
        return struct.pack("!HB", self.rank, self.suit)

    @staticmethod
    def decode3(card3: bytes) -> "Card":
        rank, suit = struct.unpack("!HB", card3)
        return Card(rank=rank, suit=suit)

    def pretty(self) -> str:
        rank_str = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(self.rank, str(self.rank))
        suit_str = SUITS[self.suit] if 0 <= self.suit < 4 else f"Suit({self.suit})"
        return f"{rank_str} of {suit_str}"

class Deck:
    """
    a pack of 52 playing cards
    """

    def __init__(self, seed: int | None = None) -> None:
        if seed is not None:
            random.seed(seed)

        self._cards: List[Card] = [Card(rank=r, suit=s) for s in range(4) for r in RANKS]
        random.shuffle(self._cards)

    def draw(self) -> Card:
        """
        get one card from the deck, if finished, rebuilds the deck.
         """
        if not self._cards:
            self.__init__()
        return self._cards.pop()

    def remaining(self) -> int:
        return len(self._cards)

def hand_total(cards: List[Card]) -> int:
    """
    calculate the total points of a hand.
    """
    return sum(c.value() for c in cards)