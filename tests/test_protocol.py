import unittest
import struct
from common.protocol import Protocol

class TestProtocol(unittest.TestCase):
    def test_offer_pack_unpack(self):
        pkt = Protocol.pack_offer(5555, "Srv")
        name, port = Protocol.unpack_offer(pkt)
        self.assertEqual(name, "Srv")
        self.assertEqual(port, 5555)

    def test_request_pack_unpack(self):
        pkt = Protocol.pack_request(7, "TeamA")
        rounds, name = Protocol.unpack_request(pkt)
        self.assertEqual(rounds, 7)
        self.assertEqual(name, "TeamA")

    def test_payload_pack_unpack(self):
        pkt = Protocol.pack_client_payload(b"Hittt")
        decision, result, card = Protocol.unpack_payload(pkt)
        self.assertEqual(decision, b"Hittt")
        self.assertEqual(result, Protocol.RES_NOT_OVER)
        self.assertEqual(card, b"\x00\x00\x00")

    def test_server_payload(self):
        card = struct.pack("!HB", 13, 3)
        pkt = Protocol.pack_server_payload(Protocol.RES_WIN, card)
        decision, result, card3 = Protocol.unpack_payload(pkt)
        self.assertEqual(result, Protocol.RES_WIN)
        self.assertEqual(card3, card)

if __name__ == "__main__":
    unittest.main()
