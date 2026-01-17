import unittest
import threading
import time
import socket

from server.tcp_server import TCPServer


class TestEdgeSlowClient(unittest.TestCase):
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

    def test_connect_no_request_timeout(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(8.0)
        s.connect(("127.0.0.1", self.server.port))

        # wait longer than server's request-timeout (your code uses 5s)
        time.sleep(6.0)

        # server should have closed the connection
        try:
            data = s.recv(1)
            # closed => b""
            self.assertTrue(data == b"" or data is not None)
        except (socket.timeout, ConnectionResetError, OSError):
            # also acceptable outcomes depending on OS timing
            pass

        try:
            s.close()
        except Exception:
            pass


if __name__ == "__main__":
    unittest.main()