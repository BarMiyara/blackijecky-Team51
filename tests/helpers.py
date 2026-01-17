import socket
from dataclasses import dataclass
from common.protocol import Protocol

@dataclass
class Payload:
    decision: bytes
    result: int
    card3: bytes

def recv_payload(sock: socket.socket) -> Payload:
    data = Protocol.recv_exact(sock, Protocol.PAYLOAD_LEN)
    decision, result, card3 = Protocol.unpack_payload(data)
    return Payload(decision=decision, result=result, card3=card3)

def recv_until_final(sock: socket.socket, max_packets: int = 200) -> int:
    for _ in range(max_packets):
        p = recv_payload(sock)
        if p.result != Protocol.RES_NOT_OVER:
            return p.result
    raise TimeoutError("Too many packets without reaching final result")

def connect_and_request(port: int, rounds: int, name: str, timeout_sec: float = 3.0) -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout_sec)
    s.connect(("127.0.0.1", port))
    s.sendall(Protocol.pack_request(rounds, name))
    return s
