import socket
from common.protocol import Protocol
from common.cards import Card
from client.ui import ask_decision, print_result

def play_session(server_ip, tcp_port, team_name, rounds):
    wins = 0
    played = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, tcp_port))

    sock.sendall(Protocol.pack_request(rounds, team_name))

    for _ in range(rounds):
        print("\n--- New Round ---")

        for i in range(3):
            data = Protocol.recv_exact(sock, Protocol.PAYLOAD_LEN)
            _dec, result, card3 = Protocol.unpack_payload(data)

            card = Card.decode3(card3)
            if i < 2:
                print(f"Your card: {card.pretty()}")
            else:
                print(f"Dealer shows: {card.pretty()}")

        while True:
            decision = ask_decision()
            sock.sendall(Protocol.pack_client_payload(decision))

            data = Protocol.recv_exact(sock, Protocol.PAYLOAD_LEN)
            _dec, result, card3 = Protocol.unpack_payload(data)

            if result == Protocol.RES_NOT_OVER:
                card = Card.decode3(card3)
                print(f"Card received: {card.pretty()}")
                continue

            print_result(result)
            played += 1
            if result == Protocol.RES_WIN:
                wins += 1
            break

    sock.close()
    print(f"\nFinished playing {played} rounds, win rate: {wins/played:.2f}")
