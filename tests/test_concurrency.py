# tests/test_concurrency.py
import unittest
import threading
import time

from server.tcp_server import TCPServer
from common.protocol import Protocol
from tests.helpers import connect_and_request, recv_payload, recv_until_final


def play_client(port: int, name: str):
    s = connect_and_request(port, rounds=1, name=name, timeout_sec=5.0)

    for _ in range(3):
        recv_payload(s)

    s.sendall(Protocol.pack_client_payload(b"Stand"))
    recv_until_final(s)
    s.close()


class TestConcurrency(unittest.TestCase):
    def test_five_clients_parallel(self):
        stop_event = threading.Event()
        server = TCPServer("127.0.0.1", "SrvTeam", stop_event=stop_event, port=0)
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        time.sleep(0.05)

        threads = []
        for i in range(5):
            th = threading.Thread(target=play_client, args=(server.port, f"C{i}"))
            threads.append(th)
            th.start()

        for th in threads:
            th.join(timeout=5)

        stop_event.set()
        server.stop()
        time.sleep(0.05)


if __name__ == "__main__":
    unittest.main()