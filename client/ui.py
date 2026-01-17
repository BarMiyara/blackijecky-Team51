from common.protocol import Protocol

def ask_rounds():
    while True:
        try:
            rounds = int(input("Enter number of rounds (1-255): "))
            if 1 <= rounds <= 255:
                return rounds
        except ValueError:
            pass
        print("Invalid input. Please enter a number between 1 and 255.")

def ask_decision() -> bytes:
    while True:
        decision = input("Hit or stand? ").strip().lower()
        if decision in ("hit", "h"):
            return b"Hittt"
        if decision in ("stand", "s"):
            return b"Stand"
        print("Please type Hit or Stand.")

def print_result(result: int):
    if result == Protocol.RES_WIN:
        print("You WIN!")
    elif result == Protocol.RES_LOSS:
        print("You LOSE.")
    elif result == Protocol.RES_TIE:
        print("It's a TIE.")