# server/game_session.py
import socket
from typing import List

from common.cards import Deck, Card, hand_total
from common.protocol import Protocol


class GameSession:
    """
    Handles blackjack rounds over an established TCP connection.
    Protocol:
    - Server sends 3 payloads at round start: player card, player card, dealer upcard
    - Client sends payload decisions: b"Hittt" or b"Stand"
    - Server sends cards as payloads with result=RES_NOT_OVER
    - When round ends, server sends payload with result=WIN/LOSS/TIE and card=000
    """

    def __init__(self, conn: socket.socket, peer: str) -> None:
        self.conn = conn
        self.peer = peer

    def play_n_rounds(self, rounds: int) -> None:
        for r in range(1, rounds + 1):
            print(f"[{self.peer}] >>> ROUND {r}/{rounds} START")
            self.play_round()
            print(f"[{self.peer}] <<< ROUND {r}/{rounds} END")

    def play_round(self) -> int:
        deck = Deck()
        player: List[Card] = [deck.draw(), deck.draw()]
        dealer: List[Card] = [deck.draw(), deck.draw()]  # dealer[1] hidden initially

        # Send initial: player2 + dealer upcard
        self._send_card(player[0])
        self._send_card(player[1])
        self._send_card(dealer[0])

        # Player turn
        while True:
            if hand_total(player) > 21:
                self._send_result(Protocol.RES_LOSS)
                return Protocol.RES_LOSS

            decision = self._recv_decision_text()

            if decision == "Hittt":
                c = deck.draw()
                player.append(c)
                self._send_card(c)
                continue

            if decision == "Stand":
                break

            # Invalid decision => treat as Stand (robustness)
            break

        # Dealer reveal + hits
        self._send_card(dealer[1])

        while hand_total(dealer) < 17:
            c = deck.draw()
            dealer.append(c)
            self._send_card(c)

        # Decide winner
        p = hand_total(player)
        d = hand_total(dealer)

        if d > 21:
            self._send_result(Protocol.RES_WIN)
            return Protocol.RES_WIN

        if p > d:
            self._send_result(Protocol.RES_WIN)
            return Protocol.RES_WIN
        if d > p:
            self._send_result(Protocol.RES_LOSS)
            return Protocol.RES_LOSS

        self._send_result(Protocol.RES_TIE)
        return Protocol.RES_TIE

    def _send_card(self, card: Card) -> None:
        pkt = Protocol.pack_server_payload(Protocol.RES_NOT_OVER, card.encode3())
        self.conn.sendall(pkt)

    def _send_result(self, result_code: int) -> None:
        pkt = Protocol.pack_server_payload(result_code, b"\x00\x00\x00")
        self.conn.sendall(pkt)

    def _recv_decision_text(self) -> str:
        data = Protocol.recv_exact(self.conn, Protocol.PAYLOAD_LEN)
        decision5, _result, _card3 = Protocol.unpack_payload(data)
        return decision5.decode("ascii", errors="ignore")