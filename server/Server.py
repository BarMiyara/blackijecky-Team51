import socket
import sys

from server.Tcp_Server import TCPServer
from server.Offer_Broadcaster import OfferBroadcaster


def best_ip_guess() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 -m server.server <TEAM_NAME>")
        raise SystemExit(1)

    team_name = sys.argv[1]

    tcp = TCPServer()
    broadcaster = OfferBroadcaster(team_name, tcp.port)

    ip = best_ip_guess()
    print(f"Server started, listening on IP address {ip}, TCP port {tcp.port}")

    broadcaster.start()
    tcp.serve_forever()


if __name__ == "__main__":
    main()