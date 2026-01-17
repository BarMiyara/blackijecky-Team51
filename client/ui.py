# from common.protocol import Protocol
#
#
# def ask_rounds() -> int:
#     while True:
#         try:
#             s = input("Enter number of rounds (1-255): ").strip()
#         except KeyboardInterrupt:
#             # let main() handle it nicely
#             raise
#
#         try:
#             rounds = int(s)
#             if 1 <= rounds <= 255:
#                 return rounds
#         except ValueError:
#             pass
#
#         print("Please enter an integer between 1 and 255.")
#
# def ask_decision() -> bytes:
#     """
#     Returns exactly 5 bytes: b'Hittt' or b'Stand'
#     Accepts: hit/Hit/h, stand/Stand/s
#     """
#     while True:
#         ans = input("Hit or stand? ").strip().lower()
#         if ans in ("hit", "h"):
#             return b"Hittt"
#         if ans in ("stand", "s"):
#             return b"Stand"
#         print("Please type Hit or Stand.")
#
#
# def print_result(result: int) -> None:
#     if result == Protocol.RES_WIN:
#         print("You WIN!")
#     elif result == Protocol.RES_LOSS:
#         print("You LOSE.")
#     elif result == Protocol.RES_TIE:
#         print("It's a TIE.")
#     else:
#         print("Round status: not over.")


# client/ui.py
from common.cards import Card, hand_total

SUIT_SYMBOL = {
    0: "♥",
    1: "♦",
    2: "♣",
    3: "♠"
}

RESULT_TEXT = {
    0: ("⏳ Round continues...", ""),
    1: ("🤝 TIE!", "Dealer and you tied."),
    2: ("💀 LOSS!", "Dealer wins this round."),
    3: ("🏆 WIN!", "You win this round!")
}


def render_card_ascii(card: Card) -> list[str]:
    rank = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(card.rank, str(card.rank))
    suit = SUIT_SYMBOL.get(card.suit, "?")

    # align rank for 10 (two chars)
    left = rank.ljust(2)
    right = rank.rjust(2)

    return [
        "┌─────────┐",
        f"│ {left}      │",
        "│         │",
        f"│    {suit}    │",
        "│         │",
        f"│      {right} │",
        "└─────────┘"
    ]


def render_hidden_card() -> list[str]:
    return [
        "┌─────────┐",
        "│░░░░░░░░░│",
        "│░░░░░░░░░│",
        "│░░░░░░░░░│",
        "│░░░░░░░░░│",
        "│░░░░░░░░░│",
        "└─────────┘"
    ]


def render_hand(cards: list[Card], hide_first: bool = False) -> str:
    blocks = []
    for i, c in enumerate(cards):
        if hide_first and i == 0:
            blocks.append(render_hidden_card())
        else:
            blocks.append(render_card_ascii(c))

    # merge side-by-side
    lines = []
    for row in range(7):
        lines.append("  ".join(block[row] for block in blocks))
    return "\n".join(lines)


def risk_meter(total: int) -> str:
    if total > 21:
        return "💀 BUST"
    if total == 21:
        return "🏆 PERFECT 21"
    if total >= 17:
        return "🔥 HIGH RISK"
    if total >= 12:
        return "⚠️ MEDIUM"
    return "✅ SAFE"


def print_hud(round_idx: int, rounds: int, wins: int, losses: int, ties: int,
              dealer_cards: list[Card], player_cards: list[Card], hide_dealer: bool = True):
    print("\n" + "═" * 45)
    print(f"🎮 Round {round_idx}/{rounds}   🏆 Wins: {wins}   💀 Losses: {losses}   🤝 Ties: {ties}")
    print("═" * 45)

    player_total = hand_total(player_cards)
    print("\nDealer:")
    print(render_hand(dealer_cards, hide_first=hide_dealer))

    print("\nYou:")
    print(render_hand(player_cards))
    print(f"\nYour total: {player_total}   |   {risk_meter(player_total)}")


def ask_decision() -> bytes:
    while True:
        ans = input("\nChoose action [Hit/Stand]: ").strip().lower()
        if ans in ("hit", "h"):
            return b"Hittt"
        if ans in ("stand", "s"):
            return b"Stand"
        print("❌ Invalid input. Please type Hit or Stand.")

def ask_rounds() -> int:
    while True:
        s = input("Enter number of rounds (1-255): ").strip()
        try:
            n = int(s)
        except ValueError:
            print("❌ Please enter a number.")
            continue
        if 1 <= n <= 255:
            return n
        print("❌ Rounds must be between 1 and 255.")

def print_result(result_code: int):
    title, msg = RESULT_TEXT.get(result_code, ("❓ Unknown result", ""))
    print("\n" + "═" * 45)
    print(title)
    if msg:
        print(msg)
    print("═" * 45)


def print_summary(rounds: int, wins: int, losses: int, ties: int):
    win_rate = wins / rounds if rounds > 0 else 0.0
    non_loss = (wins + ties) / rounds if rounds > 0 else 0.0

    print("\n" + "═" * 35)
    print("📊 GAME SUMMARY")
    print("═" * 35)
    print(f"Rounds played : {rounds}")
    print(f"Wins          : {wins}")
    print(f"Losses        : {losses}")
    print(f"Ties          : {ties}")
    print(f"Win rate      : {win_rate*100:.1f}%")
    print(f"Non-loss rate : {non_loss*100:.1f}%")
    print("═" * 35)