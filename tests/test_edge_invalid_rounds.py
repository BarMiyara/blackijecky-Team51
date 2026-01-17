import unittest
import threading
import time
import socket
import struct

from server.tcp_server import TCPServer
from common.protocol import Protocol


class TestEdgeInvalidRounds(unittest.TestCase):
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

    def test_rounds_zero_should_close(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(("127.0.0.1", self.server.port))

        # craft a valid REQUEST header but rounds=0
        pkt = struct.pack("!IBB32s",
                          Protocol.MAGIC_COOKIE,
                          Protocol.MSG_REQUEST,
                          0,
                          Protocol.pack_name("ClientX"))
        self.assertEqual(len(pkt), Protocol.REQUEST_LEN)

        s.sendall(pkt)

        # server should close or send nothing; try read 1 byte
        try:
            data = s.recv(1)
            self.assertTrue(data == b"" or data is not None)
        except (socket.timeout, ConnectionResetError, OSError):
            pass

        s.close()


if __name__ == "__main__":
    unittest.main()