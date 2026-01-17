import unittest
import threading
import time

from server.tcp_server import TCPServer
from common.protocol import Protocol
from tests.helpers import connect_and_request, recv_payload


class TestEdgeInvalidDecision(unittest.TestCase):
    def setUp(self):
        self.stop_event = threading.Event()
        self.server = TCPServer("127.0.0.1", "SrvTeam", stop_event=self.stop_event, port=0)
        self.t = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.t.start()
        time.sleep(0.05)

    def tearDown(self):
        self.stop_event.set()
        self.server.stop()
        time.sleep(0.05)

    def test_invalid_decision_should_not_hang(self):
        s = connect_and_request(self.server.port, rounds=1, name="ClientBad", timeout_sec=3.0)

        # initial 3 payloads
        for _ in range(3):
            p = recv_payload(s)
            self.assertEqual(p.result, Protocol.RES_NOT_OVER)

        # send unknown decision (still 5 bytes)
        s.sendall(Protocol.pack_client_payload(b"Hello"))

        # Now: either server closes, or finishes round, or gives more cards then finishes.
        # We'll read up to 50 payloads max so test can't hang.
        for _ in range(50):
            try:
                p = recv_payload(s)
            except Exception:
                # closed/ended => acceptable
                s.close()
                return

            if p.result != Protocol.RES_NOT_OVER:
                self.assertIn(p.result, (Protocol.RES_WIN, Protocol.RES_LOSS, Protocol.RES_TIE))
                s.close()
                return

        s.close()
        self.fail("Server did not close or finish round after invalid decision (possible hang).")


if __name__ == "__main__":
    unittest.main()