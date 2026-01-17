import struct

class Protocol:
    MAGIC_COOKIE = 0xabcddcba

    MSG_OFFER = 0x2
    MSG_REQUEST = 0x3
    MSG_PAYLOAD = 0x4

    UDP_PORT = 13122

    RES_NOT_OVER = 0x0
    RES_TIE = 0x1
    RES_LOSS = 0x2
    RES_WIN = 0x3

    NAME_LEN = 32
    DECISION_LEN = 5
    CARD_LEN = 3

    OFFER_LEN = 4 + 1 + 2 + NAME_LEN
    REQUEST_LEN = 4 + 1 + 1 + NAME_LEN
    PAYLOAD_LEN = 4 + 1 + DECISION_LEN + 1 + CARD_LEN

    @staticmethod
    def pack_name(name: str) -> bytes:
        """
        changes a name string to 32 bytes
        """
        raw = name.encode("utf-8", errors="ignore")
        return raw[:Protocol.NAME_LEN].ljust(Protocol.NAME_LEN, b"\x00")

    @staticmethod
    def unpack_name(data: bytes) -> str:
        """
        change the 32 bytes back to string
        """
        return data.split(b"\x00", 1)[0].decode("utf-8", errors="ignore")

    @staticmethod
    def pack_offer(tcp_port: int, server_name: str) -> bytes:
        """
        cookie(4) | type(1) | tcp_port(2) | server_name(32)
        """
        return struct.pack(
            "!IBH32s",
            Protocol.MAGIC_COOKIE,
            Protocol.MSG_OFFER,
            tcp_port,
            Protocol.pack_name(server_name)
        )

    @staticmethod
    def unpack_offer(data: bytes) -> tuple[str, int]:
        if len(data) != Protocol.OFFER_LEN:
            raise ValueError("Invalid OFFER length")

        cookie, msg_type, tcp_port, name = struct.unpack("!IBH32s", data)

        if cookie != Protocol.MAGIC_COOKIE or msg_type != Protocol.MSG_OFFER:
            raise ValueError("Invalid OFFER header")

        return Protocol.unpack_name(name), tcp_port

    @staticmethod
    def pack_request(rounds: int, client_name: str) -> bytes:
        """
        cookie(4) | type(1) | rounds(1) | client_name(32)
        """
        if not (0 <= rounds <= 255):
            raise ValueError("Rounds must be 0-255")

        return struct.pack(
            "!IBB32s",
            Protocol.MAGIC_COOKIE,
            Protocol.MSG_REQUEST,
            rounds,
            Protocol.pack_name(client_name)
        )

    @staticmethod
    def unpack_request(data: bytes) -> tuple[int, str]:
        if len(data) != Protocol.REQUEST_LEN:
            raise ValueError("Invalid REQUEST length")

        cookie, msg_type, rounds, name = struct.unpack("!IBB32s", data)

        if cookie != Protocol.MAGIC_COOKIE or msg_type != Protocol.MSG_REQUEST:
            raise ValueError("Invalid REQUEST header")

        return rounds, Protocol.unpack_name(name)

    @staticmethod
    def pack_client_payload(decision: bytes) -> bytes:
        """
        cookie(4) | type(1) | decision(5) | result(1=0) | card(3=000)
        """
        if len(decision) != Protocol.DECISION_LEN:
            raise ValueError("Decision must be 5 bytes")

        return struct.pack(
            "!IB5sB3s",
            Protocol.MAGIC_COOKIE,
            Protocol.MSG_PAYLOAD,
            decision,
            Protocol.RES_NOT_OVER,
            b"\x00\x00\x00"
        )

    @staticmethod
    def pack_server_payload(result: int, card: bytes) -> bytes:
        """
        cookie(4) | type(1) | decision(00000) | result(1) | card(3)
        """
        if len(card) != Protocol.CARD_LEN:
            raise ValueError("Card must be 3 bytes")

        return struct.pack(
            "!IB5sB3s",
            Protocol.MAGIC_COOKIE,
            Protocol.MSG_PAYLOAD,
            b"\x00" * Protocol.DECISION_LEN,
            result,
            card
        )

    @staticmethod
    def unpack_payload(data: bytes) -> tuple[bytes, int, bytes]:
        if len(data) != Protocol.PAYLOAD_LEN:
            raise ValueError("Invalid PAYLOAD length")

        cookie, msg_type, decision, result, card = struct.unpack("!IB5sB3s", data)

        if cookie != Protocol.MAGIC_COOKIE or msg_type != Protocol.MSG_PAYLOAD:
            raise ValueError("Invalid PAYLOAD header")
        return decision, result, card

    @staticmethod
    def recv_exact(sock, size: int) -> bytes:
        """
        read size bytes from the tcp socket
        """
        data = b""
        while len(data) < size:
            chunk = sock.recv(size - len(data))
            if not chunk:
                raise ConnectionError("Socket closed")
            data += chunk
        return data