import unittest
from common.cards import Card, Deck, hand_total

class TestCards(unittest.TestCase):
    def test_card_values(self):
        self.assertEqual(Card(1, 0).value(), 11)
        self.assertEqual(Card(11, 0).value(), 10)
        self.assertEqual(Card(12, 0).value(), 10)
        self.assertEqual(Card(13, 0).value(), 10)
        self.assertEqual(Card(10, 0).value(), 10)
        self.assertEqual(Card(2, 0).value(), 2)

    def test_encode_decode(self):
        c = Card(7, 2)
        b = c.encode3()
        c2 = Card.decode3(b)
        self.assertEqual(c, c2)

    def test_deck_draw_52_unique(self):
        d = Deck(seed=123)
        seen = set()
        for _ in range(52):
            c = d.draw()
            seen.add((c.rank, c.suit))
        self.assertEqual(len(seen), 52)

    def test_hand_total(self):
        self.assertEqual(hand_total([Card(1, 0), Card(13, 1)]), 21)

if __name__ == "__main__":
    unittest.main()
