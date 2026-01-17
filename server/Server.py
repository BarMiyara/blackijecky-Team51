import socket
import threading

from server.tcp_server import TCPServer
from server.offer_broadcaster import OfferBroadcaster


def best_ip_guess() -> str:
    """
    Tries to guess local LAN IP by opening a UDP socket to a public address (no packets are actually sent).
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"


class ServerApp:
    """
    Coordinates UDP offer broadcasting + TCP game server.
    Handles clean shutdown on Ctrl+C.
    """
    def __init__(self, team_name: str) -> None:
        self.team_name = team_name
        self.ip = best_ip_guess()

        self._stop_event = threading.Event()

        # TCP server picks a port (or you can pass one). Offer broadcaster will advertise it.
        self.tcp_server = TCPServer(self.ip, team_name, stop_event=self._stop_event)

        # IMPORTANT: Offer broadcaster needs the TCP port to advertise
        self.offer = OfferBroadcaster(self.ip, self.tcp_server.port, team_name, stop_event=self._stop_event)

    def start(self) -> None:
        # Start UDP offers + TCP server
        self.offer.start()
        self.tcp_server.serve_forever()

    def stop(self) -> None:
        # Signal everyone to stop
        self._stop_event.set()

        # Stop TCP first (unblocks accept)
        try:
            self.tcp_server.stop()
        except Exception:
            pass

        # Stop offer broadcaster
        try:
            self.offer.stop()
        except Exception:
            pass


def main(team_name: str) -> None:
    app = ServerApp(team_name)
    try:
        app.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        app.stop()


if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "ServerTeam"
    main(name)