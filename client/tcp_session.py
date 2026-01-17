# import socket
# from common.protocol import Protocol
# from common.cards import Card, hand_total
# from client.ui import ask_decision, print_result, print_hud, print_summary
#
#
# def play_session(server_ip: str, tcp_port: int, team_name: str, rounds: int) -> None:
#     wins = 0
#     played = 0
#
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.settimeout(5)
#     sock.connect((server_ip, tcp_port))
#     sock.settimeout(None)
#
#     sock.sendall(Protocol.pack_request(rounds, team_name))
#
#     for _ in range(rounds):
#         print("\n--- New Round ---")
#
#         player_cards = []
#         stood = False
#         busted = False
#
#         # Expect 3 payloads: 2 player cards + 1 dealer upcard
#         for i in range(3):
#             data = Protocol.recv_exact(sock, Protocol.PAYLOAD_LEN)
#             _dec, result, card3 = Protocol.unpack_payload(data)
#
#             if result != Protocol.RES_NOT_OVER:
#                 # Defensive: round ended unexpectedly
#                 print_result(result)
#                 played += 1
#                 if result == Protocol.RES_WIN:
#                     wins += 1
#                 break
#
#             card = Card.decode3(card3)
#             if i < 2:
#                 player_cards.append(card)
#                 print(f"Your card: {card.pretty()}")
#             else:
#                 print(f"Dealer shows: {card.pretty()}")
#
#         # Main loop: decisions + receiving server stream
#         while True:
#             # IMPORTANT:
#             # - if busted: stop sending decisions, just read until final result arrives
#             # - if stood: stop sending decisions, just read dealer cards until final result
#             if not stood and not busted:
#                 decision = ask_decision()
#                 try:
#                     sock.sendall(Protocol.pack_client_payload(decision))
#                 except (BrokenPipeError, ConnectionResetError, OSError):
#                     print("Connection closed by server.")
#                     sock.close()
#                     return
#
#                 if decision == b"Stand":
#                     stood = True
#
#             data = Protocol.recv_exact(sock, Protocol.PAYLOAD_LEN)
#             _dec, result, card3 = Protocol.unpack_payload(data)
#
#             if result == Protocol.RES_NOT_OVER:
#                 card = Card.decode3(card3)
#
#                 if stood:
#                     # Dealer stream after Stand (reveal + hits)
#                     print(f"Dealer card: {card.pretty()}")
#                 else:
#                     # Player hit card
#                     player_cards.append(card)
#                     print(f"Card received: {card.pretty()}")
#
#                     # Local bust detection prevents sending extra decisions
#                     if hand_total(player_cards) > 21:
#                         busted = True
#
#                 continue
#
#             # Round ended
#             print_result(result)
#             played += 1
#             if result == Protocol.RES_WIN:
#                 wins += 1
#             break
#
#     sock.close()
#     if played == 0:
#         print("\nFinished playing 0 rounds, win rate: 0.00")
#     else:
#         print(f"\nFinished playing {played} rounds, win rate: {wins/played:.2f}")




# client/tcp_session.py
import socket

from common.protocol import Protocol
from common.cards import Card, hand_total
from client.ui import ask_decision, print_result, print_hud, print_summary

DECISION_HIT = b"Hittt"
DECISION_STAND = b"Stand"


def _safe_close(sock: socket.socket) -> None:
    try:
        sock.shutdown(socket.SHUT_RDWR)
    except Exception:
        pass
    try:
        sock.close()
    except Exception:
        pass


def play_session(server_ip: str, tcp_port: int, team_name: str, rounds: int) -> None:
    wins = losses = ties = played = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.settimeout(5.0)
        sock.connect((server_ip, tcp_port))
        sock.settimeout(None)

        sock.sendall(Protocol.pack_request(rounds, team_name))

        for round_idx in range(1, rounds + 1):
            player_cards: list[Card] = []
            dealer_cards: list[Card] = []
            stood = False
            busted = False

            # Initial deal: 2 player + 1 dealer upcard
            for i in range(3):
                data = Protocol.recv_exact(sock, Protocol.PAYLOAD_LEN)
                _dec, result, card3 = Protocol.unpack_payload(data)

                if result != Protocol.RES_NOT_OVER:
                    print_result(result)
                    played += 1
                    if result == Protocol.RES_WIN:
                        wins += 1
                    elif result == Protocol.RES_LOSS:
                        losses += 1
                    elif result == Protocol.RES_TIE:
                        ties += 1
                    break

                card = Card.decode3(card3)
                if i < 2:
                    player_cards.append(card)
                else:
                    dealer_cards.append(card)

            print_hud(round_idx, rounds, wins, losses, ties, dealer_cards, player_cards, hide_dealer=False)

            while True:
                # After bust or stand: never send more decisions
                if not stood and not busted:
                    decision = ask_decision()
                    if decision not in (DECISION_HIT, DECISION_STAND):
                        decision = DECISION_STAND

                    try:
                        sock.sendall(Protocol.pack_client_payload(decision))
                    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
                        # Server likely closed because the round already ended (e.g., bust)
                        busted = True

                    if decision == DECISION_STAND:
                        stood = True

                try:
                    data = Protocol.recv_exact(sock, Protocol.PAYLOAD_LEN)
                except (ConnectionError, OSError):
                    # Connection ended unexpectedly; stop this session cleanly
                    return

                _dec, result, card3 = Protocol.unpack_payload(data)

                if result == Protocol.RES_NOT_OVER:
                    card = Card.decode3(card3)

                    if stood:
                        dealer_cards.append(card)
                    else:
                        player_cards.append(card)

                        # Local bust detection: prevents sending any further decisions
                        if hand_total(player_cards) > 21:
                            busted = True

                    print_hud(round_idx, rounds, wins, losses, ties, dealer_cards, player_cards, hide_dealer=False)
                    continue

                print_result(result)
                played += 1
                if result == Protocol.RES_WIN:
                    wins += 1
                elif result == Protocol.RES_LOSS:
                    losses += 1
                elif result == Protocol.RES_TIE:
                    ties += 1
                break

    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError, ConnectionError) as e:
        print(f"Connection error: {e}")

    finally:
        _safe_close(sock)
        print_summary(played, wins, losses, ties)