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
        # Assignment rules: Ace is always 11
        if self.rank == 1:
            return 11
        if self.rank >= 11:
            return 10
        return self.rank

    def encode3(self) -> bytes:
        # 2 bytes rank (01-13), 1 byte suit (0-3)
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
    """A pack of 52 playing cards."""

    def __init__(self, seed: int | None = None) -> None:
        # Use a private RNG so we don't affect global random state
        self._rng = random.Random(seed)
        self._cards: List[Card] = [Card(rank=r, suit=s) for s in range(4) for r in RANKS]
        self._rng.shuffle(self._cards)

    def draw(self) -> Card:
        """Draw one card; if deck is empty, rebuild a fresh shuffled deck."""
        if not self._cards:
            self.__init__()  # fresh deck (non-deterministic)
        return self._cards.pop()

    def remaining(self) -> int:
        return len(self._cards)


def hand_total(cards: List[Card]) -> int:
    """
    Calculate the total points of a hand.
    Ace is always 11 (per assignment rules).
    """
    total = 0
    for c in cards:
        if not (1 <= c.rank <= 13):
            raise ValueError(f"Invalid rank: {c.rank}")
        if not (0 <= c.suit <= 3):
            raise ValueError(f"Invalid suit: {c.suit}")
        total += c.value()
    return total