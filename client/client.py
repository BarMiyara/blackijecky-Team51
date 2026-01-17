import sys
from client.udp_listener import listen_for_offer
from client.tcp_session import play_session
from client.ui import ask_rounds

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 -m client.client <TEAM_NAME>")
        return

    team_name = sys.argv[1]

    while True:
        rounds = ask_rounds()
        server_ip, tcp_port = listen_for_offer()
        play_session(server_ip, tcp_port, team_name, rounds)

if __name__ == "__main__":
    main()