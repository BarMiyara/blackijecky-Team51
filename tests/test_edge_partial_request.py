import unittest
import threading
import time
import socket

from server.tcp_server import TCPServer
from common.protocol import Protocol


class TestEdgePartialRequest(unittest.TestCase):
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

    def test_partial_request_then_disconnect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(("127.0.0.1", self.server.port))

        # send only half of REQUEST_LEN then close
        half = Protocol.REQUEST_LEN // 2
        s.sendall(b"\x00" * half)
        s.close()

        # give server handler time to exit; test passes if no hang / exception bubbles here
        time.sleep(0.2)


if __name__ == "__main__":
    unittest.main()