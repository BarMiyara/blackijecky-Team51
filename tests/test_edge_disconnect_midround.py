import unittest
import threading
import time

from server.tcp_server import TCPServer
from common.protocol import Protocol
from tests.helpers import connect_and_request, recv_payload


class TestEdgeDisconnectMidround(unittest.TestCase):
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

    def test_disconnect_after_hit(self):
        s = connect_and_request(self.server.port, rounds=1, name="Quitter", timeout_sec=3.0)

        # initial 3 payloads
        for _ in range(3):
            recv_payload(s)

        # send hit then disconnect immediately
        s.sendall(Protocol.pack_client_payload(b"Hittt"))
        s.close()

        # give server time to clean up thread
        time.sleep(0.2)


if __name__ == "__main__":
    unittest.main()