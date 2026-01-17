import socket
from common.protocol import Protocol


def wait_for_offer() -> tuple[str, int]:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except OSError:
        pass

    s.bind(("", Protocol.UDP_PORT))

    while True:
        data, addr = s.recvfrom(2048)
        try:
            _server_name, tcp_port = Protocol.unpack_offer(data)
            server_ip = addr[0]
            return server_ip, tcp_port
        except Exception:
            continue