# tests/test_tcp_smoke.py
import unittest
import threading
import time

from server.tcp_server import TCPServer
from common.protocol import Protocol
from tests.helpers import connect_and_request, recv_payload, recv_until_final


class TestTCPSmoke(unittest.TestCase):
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

    def test_one_round_stand(self):
        s = connect_and_request(self.server.port, rounds=1, name="ClientA")

        # 3 initial payloads
        for _ in range(3):
            p = recv_payload(s)
            self.assertEqual(p.result, Protocol.RES_NOT_OVER)

        # Stand
        s.sendall(Protocol.pack_client_payload(b"Stand"))

        # until final
        final_res = recv_until_final(s)
        self.assertIn(final_res, (Protocol.RES_WIN, Protocol.RES_LOSS, Protocol.RES_TIE))
        s.close()

    def test_three_rounds_stand(self):
        s = connect_and_request(self.server.port, rounds=3, name="ClientB")

        for _round in range(3):
            for _ in range(3):
                p = recv_payload(s)
                self.assertEqual(p.result, Protocol.RES_NOT_OVER)

            s.sendall(Protocol.pack_client_payload(b"Stand"))
            final = recv_until_final(s)
            self.assertIn(final, (Protocol.RES_WIN, Protocol.RES_LOSS, Protocol.RES_TIE))

        s.close()


if __name__ == "__main__":
    unittest.main()