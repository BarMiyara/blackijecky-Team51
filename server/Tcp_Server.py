import socket
import threading

from common.protocol import Protocol
from server.Game_Session import GameSession


class TCPServer:
    REQUEST_LEN = 4 + 1 + 1 + 32

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", 0))  # ephemeral
        self.sock.listen(50)
        self.port = self.sock.getsockname()[1]

    def serve_forever(self) -> None:
        while True:
            conn, addr = self.sock.accept()
            threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True).start()

    def _handle_client(self, conn: socket.socket, addr) -> None:
        peer = f"{addr[0]}:{addr[1]}"
        try:
            req = Protocol.recv_exact(conn, self.REQUEST_LEN)
            rounds, client_name = Protocol.unpack_request(req)

            print(f"[{peer}] {client_name} requested {rounds} rounds")

            session = GameSession(conn, peer)
            for i in range(rounds):
                session.play_round()

        except Exception as e:
            print(f"[{peer}] Error: {e}")
        finally:
            try:
                conn.close()
            except Exception:
                pass