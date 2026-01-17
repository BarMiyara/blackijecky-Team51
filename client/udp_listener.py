import socket
from common.protocol import Protocol

def listen_for_offer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except Exception:
        pass

    sock.bind(('', Protocol.UDP_PORT))
    print("Client started, listening for offer requests...")

    while True:
        data, addr = sock.recvfrom(1024)
        try:
            server_name, tcp_port = Protocol.unpack_offer(data)
            server_ip = addr[0]
            print(f"Received offer from {server_ip}")
            sock.close()
            return server_ip, tcp_port
        except Exception:
            continue