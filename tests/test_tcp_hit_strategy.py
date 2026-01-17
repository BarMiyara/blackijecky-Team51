# tests/test_tcp_hit_strategy.py
import unittest
import threading
import time

from server.tcp_server import TCPServer
from common.protocol import Protocol
from tests.helpers import connect_and_request, recv_payload, recv_until_final


class TestTCPHitStrategy(unittest.TestCase):
    def setUp(self):
        self.stop_event = threading.Event()
        self.server = TCPServer("127.0.0.1", "SrvTeam", stop_event=self.stop_event, port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        time.sleep(0.05)

    def tearDown(self):
        self.stop_event.set()
        self.server.stop()
        time.sleep(0.05)

    def test_hit_then_stand(self):
        s = connect_and_request(self.server.port, rounds=1, name="Hitter")

        # initial
        for _ in range(3):
            self.assertEqual(recv_payload(s).result, Protocol.RES_NOT_OVER)

        # hit up to 5 times max (כדי לא להיתקע)
        for _ in range(5):
            s.sendall(Protocol.pack_client_payload(b"Hittt"))
            p = recv_payload(s)

            if p.result != Protocol.RES_NOT_OVER:
                # round ended (bust or dealer logic finished)
                self.assertIn(p.result, (Protocol.RES_WIN, Protocol.RES_LOSS, Protocol.RES_TIE))
                s.close()
                return

            # got a card, continue

        # אם לא נגמר—Stand ואז לוודא שנגמר
        s.sendall(Protocol.pack_client_payload(b"Stand"))
        final = recv_until_final(s)
        self.assertIn(final, (Protocol.RES_WIN, Protocol.RES_LOSS, Protocol.RES_TIE))
        s.close()


if __name__ == "__main__":
    unittest.main()