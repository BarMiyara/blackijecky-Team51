import socket
import threading
import time
from typing import Optional

from common.protocol import Protocol


class OfferBroadcaster(threading.Thread):
    """
    Broadcasts UDP "offer" packets once per second on Protocol.UDP_PORT.
    Clean shutdown supported via stop_event or stop().
    """

    def __init__(
        self,
        server_ip: str,
        tcp_port: int,
        team_name: str,
        stop_event: Optional[threading.Event] = None,
    ) -> None:
        super().__init__(daemon=True)

        self.server_ip = server_ip
        self.tcp_port = int(tcp_port)
        self.team_name = team_name

        self._stop_event = stop_event if stop_event is not None else threading.Event()

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # On some systems it helps to bind; on others it's optional.
        # Binding to "" lets OS choose interface; we only SEND anyway.
        try:
            self._sock.bind(("", 0))
        except OSError:
            pass

    def stop(self) -> None:
        """Ask the broadcaster thread to stop."""
        self._stop_event.set()

    def run(self) -> None:
        while not self._stop_event.is_set():
            try:
                pkt = Protocol.pack_offer(self.tcp_port, self.team_name)
                self._sock.sendto(pkt, ("<broadcast>", Protocol.UDP_PORT))
            except Exception:
                # Never crash the server because broadcast failed momentarily
                pass

            # Sleep ~1 second, but allow fast exit
            for _ in range(10):
                if self._stop_event.is_set():
                    break
                time.sleep(0.1)

        try:
            self._sock.close()
        except Exception:
            pass