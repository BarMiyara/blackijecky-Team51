import socket
from common.protocol import (pack_request, pack_payload_client_decision, unpack_payload, recv_exact, RES_NOT_OVER, RES_WIN)
from common.cards import Card
from client.ui import ask_decision, print_result

PAYLOAD_SIZE = 14

def play_session(server_ip, tcp_port, team_name, rounds):
    wins = 0
    played = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, tcp_port))

    sock.sendall(pack_request(rounds, team_name))

    for _ in range(rounds):
        print("\n--- New Round ---")

        # קבלת קלפים התחלתיים
        for i in range(3):
            data = recv_exact(sock, PAYLOAD_SIZE)
            _, _, card3 = unpack_payload(data)
            card = Card.decode3(card3)
            if i < 2:
                print(f"Your card: {card.pretty()}")
            else:
                print(f"Dealer shows: {card.pretty()}")

        # תור השחקן
        while True:
            decision = ask_decision()
            sock.sendall(pack_payload_client_decision(decision))

            data = recv_exact(sock, PAYLOAD_SIZE)
            _, result, card3 = unpack_payload(data)

            if result == RES_NOT_OVER:
                card = Card.decode3(card3)
                print(f"Card received: {card.pretty()}")
                continue

            print_result(result)
            played += 1
            if result == RES_WIN:
                wins += 1
            break

    sock.close()
    print(f"\nFinished playing {played} rounds, win rate: {wins / played:.2f}")
