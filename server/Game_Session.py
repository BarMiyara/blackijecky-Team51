import socket
from typing import List

from common.cards import Deck, Card, hand_total
from common.protocol import (
    RES_LOSS, RES_WIN, RES_TIE, RES_NOT_OVER,
    pack_payload_server, unpack_payload, recv_exact
)


class GameSession:
    PAYLOAD_LEN = 4 + 1 + 5 + 1 + 3

    def __init__(self, conn: socket.socket, peer: str) -> None:
        self.conn = conn
        self.peer = peer

    def play_round(self) -> int:
        deck = Deck()
        player: List[Card] = [deck.draw(), deck.draw()]
        dealer: List[Card] = [deck.draw(), deck.draw()]  # dealer[1] hidden at first

        # Send initial: player2 + dealer upcard
        self._send_card(player[0])
        self._send_card(player[1])
        self._send_card(dealer[0])

        # Player turn
        while True:
            if hand_total(player) > 21:
                self._send_result(RES_LOSS)
                return RES_LOSS

            decision = self._recv_decision_text()
            if decision == "Hittt":
                c = deck.draw()
                player.append(c)
                self._send_card(c)
                continue
            # treat anything else as Stand (including invalid)
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
            self._send_result(RES_WIN)
            return RES_WIN

        if p > d:
            self._send_result(RES_WIN)
            return RES_WIN
        if d > p:
            self._send_result(RES_LOSS)
            return RES_LOSS

        self._send_result(RES_TIE)
        return RES_TIE

    def _send_card(self, card: Card) -> None:
        pkt = pack_payload_server(RES_NOT_OVER, card.encode3())
        self.conn.sendall(pkt)

    def _send_result(self, result_code: int) -> None:
        pkt = pack_payload_server(result_code, b"\x00\x00\x00")
        self.conn.sendall(pkt)

    def _recv_decision_text(self) -> str:
        data = recv_exact(self.conn, self.PAYLOAD_LEN)
        decision5, _result, _card3 = unpack_payload(data)
        return decision5.decode("ascii", errors="ignore")