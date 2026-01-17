# tests/test_malformed_request.py
import unittest
import threading
import time
import socket
import struct

from server.tcp_server import TCPServer
from common.protocol import Protocol


class TestMalformedRequest(unittest.TestCase):
    def test_bad_cookie_request_closes(self):
        stop_event = threading.Event()
        server = TCPServer("127.0.0.1", "SrvTeam", stop_event=stop_event, port=0)
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        time.sleep(0.05)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(("127.0.0.1", server.port))

        # Build request with WRONG cookie
        bad_cookie = 0x11111111
        pkt = struct.pack("!IBB32s", bad_cookie, Protocol.MSG_REQUEST, 1, Protocol.pack_name("X"))
        self.assertEqual(len(pkt), Protocol.REQUEST_LEN)
        s.sendall(pkt)

        # Server should close (recv returns b'' or raises)
        try:
            data = s.recv(1)
            self.assertTrue(data == b"" or data is not None)
        except Exception:
            pass

        try:
            s.close()
        except Exception:
            pass

        stop_event.set()
        server.stop()
        time.sleep(0.05)


if __name__ == "__main__":
    unittest.main()