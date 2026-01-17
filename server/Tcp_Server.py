# server/tcp_server.py
import socket
import threading
import traceback

from common.protocol import Protocol
from server.game_session import GameSession


class TCPServer:
    def __init__(self, ip: str, team_name: str, stop_event: threading.Event, port: int = 0):
        self.ip = ip
        self.team_name = team_name
        self._stop_event = stop_event

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, port))
        self.sock.listen()
        self.sock.settimeout(1.0)  # so we can exit cleanly when stop_event is set

        self.port = self.sock.getsockname()[1]
        print(f"Server started, listening on IP address {self.ip}, TCP port {self.port}")

    def serve_forever(self):
        while not self._stop_event.is_set():
            try:
                conn, addr = self.sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            t = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
            t.start()

    def stop(self):
        try:
            self.sock.close()
        except Exception:
            pass

    def handle_client(self, conn: socket.socket, addr):
        peer = f"{addr[0]}:{addr[1]}"
        try:
            conn.settimeout(5.0)

            req = Protocol.recv_exact(conn, Protocol.REQUEST_LEN)

            try:
                rounds, client_name = Protocol.unpack_request(req)
            except ValueError as e:
                print(f"[{peer}] Bad request: {e} (closing)")
                return

            print(f"[{peer}] {client_name} requested {rounds} rounds")

            if not (1 <= rounds <= 255):
                print(f"[{peer}] invalid rounds={rounds}, closing")
                return

            conn.settimeout(None)

            session = GameSession(conn, peer)

            for i in range(1, rounds + 1):
                print(f"[{peer}] >>> ROUND {i}/{rounds} START")
                session.play_round()
                print(f"[{peer}] <<< ROUND {i}/{rounds} END")

            print(f"[{peer}] DONE all rounds, closing socket")

        except (ConnectionError, BrokenPipeError, ConnectionResetError) as e:
            print(f"[{peer}] Connection ended: {e}")

        except socket.timeout:
            print(f"[{peer}] Timeout waiting for REQUEST, closing")

        except Exception as e:
            print(f"[{peer}] ERROR: {e}")
            traceback.print_exc()

        finally:
            try:
                conn.close()
            except Exception:
                pass