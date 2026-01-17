# from client.udp_listener import wait_for_offer
# from client.tcp_session import play_session
# # from client.ui import ask_rounds
# from client.ui import ask_decision, print_result, print_hud, print_summary
#
#
# def main(team_name: str) -> None:
#     print("Client started.")
#     try:
#         while True:
#             try:
#                 rounds = ask_rounds()
#             except KeyboardInterrupt:
#                 print("\nClient shutting down. Bye!")
#                 return
#
#             print("Listening for offer requests... (Ctrl+C to quit)")
#
#             try:
#                 server_ip, tcp_port = wait_for_offer()
#             except KeyboardInterrupt:
#                 print("\nClient shutting down. Bye!")
#                 return
#             except Exception as e:
#                 print(f"UDP listener error: {e}")
#                 continue
#
#             print(f"Received offer from {server_ip}")
#
#             try:
#                 play_session(server_ip, tcp_port, team_name, rounds)
#             except KeyboardInterrupt:
#                 print("\nClient shutting down. Bye!")
#                 return
#             except Exception as e:
#                 print(f"Connection error: {e}")
#
#             print("Returning to listening for offers...")
#
#     except KeyboardInterrupt:
#         # safety net
#         print("\nClient shutting down. Bye!")
#
#
# if __name__ == "__main__":
#     import sys
#     name = sys.argv[1] if len(sys.argv) > 1 else "Team"
#     main(name)

from client.udp_listener import wait_for_offer
from client.tcp_session import play_session
from client.ui import ask_rounds


def main(team_name: str) -> None:
    print("Client started.")
    try:
        while True:
            try:
                rounds = ask_rounds()
            except KeyboardInterrupt:
                print("\nClient shutting down. Bye!")
                return

            print("Listening for offer requests... (Ctrl+C to quit)")

            try:
                server_ip, tcp_port = wait_for_offer()
            except KeyboardInterrupt:
                print("\nClient shutting down. Bye!")
                return
            except Exception as e:
                print(f"UDP listener error: {e}")
                continue

            print(f"Received offer from {server_ip}")

            try:
                play_session(server_ip, tcp_port, team_name, rounds)
            except KeyboardInterrupt:
                print("\nClient shutting down. Bye!")
                return
            except Exception as e:
                print(f"Connection error: {e}")

            print("Returning to listening for offers...")

    except KeyboardInterrupt:
        print("\nClient shutting down. Bye!")


if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "Team"
    main(name)