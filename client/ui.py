def ask_rounds():
    while True:
        try:
            rounds = int(input("Enter number of rounds (1-255): "))
            if 1 <= rounds <= 255:
                return rounds
        except ValueError:
            pass
        print("Invalid input.")

def ask_decision():
    while True:
        choice = input("Hit or stand? ").strip().lower()
        if choice in ('hit', 'h'):
            return b'Hittt'
        if choice in ('stand', 's'):
            return b'Stand'
        print("Please type Hit or Stand.")

def print_result(result):
    if result == 0x3:
        print("You WIN!")
    elif result == 0x2:
        print("You LOSE.")
    elif result == 0x1:
        print("TIE.")