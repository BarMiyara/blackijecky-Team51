# server/offer_broadcaster.py
import socket
import threading
import time

from common.protocol import UDP_PORT, pack_offer


class OfferBroadcaster:
    def __init__(self, team_name: str, tcp_port: int) -> None:
        self.team_name = team_name
        self.tcp_port = tcp_port
        self._stop = threading.Event()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self) -> None:
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self) -> None:
        self._stop.set()
        try:
            self.sock.close()
        except Exception:
            pass

    def _loop(self) -> None:
        pkt = pack_offer(self.tcp_port, self.team_name)
        while not self._stop.is_set():
            try:
                self.sock.sendto(pkt, ("255.255.255.255", UDP_PORT))
            except Exception:
                pass
            time.sleep(1.0)