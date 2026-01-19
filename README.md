# 🃏 BlackiJecky — Team51
### UDP Discovery • TCP Sessions • Protocol-Driven Blackjack • Edge-Case Tested

<div align="center">

**Client–server Blackjack in Python**  
Server discovery via **UDP offers**, gameplay over **TCP sessions**, shared **protocol layer**, and a **serious test suite**.

<br/>

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Networking](https://img.shields.io/badge/Networking-UDP%20Discovery%20%2B%20TCP%20Sessions-purple)
![Tests](https://img.shields.io/badge/Tests-pytest-brightgreen)
![Status](https://img.shields.io/badge/Status-stable-success)

</div>

---

## 🎬 Demo
> Add a screenshot/GIF here for instant “wow”.

```md
![Demo](assets/demo.png)
⚡ What is this?
BlackiJecky is a Python client–server Blackjack project built like a real networking app:

✅ UDP discovery — the server broadcasts offers, clients can auto-detect and join

✅ TCP sessions — reliable gameplay communication per client/session

✅ Shared common/ layer — protocol + card logic used by both ends

✅ Terminal UI — clean round stats, hands, totals, and actions

✅ Edge-case tested — malformed input, partial reads, slow client, disconnect mid-round, concurrency

🧠 Architecture
Flow (UDP → TCP)
text
Copy code
         UDP Broadcast (Offer)
Server  ----------------------->  Client
  |                                  |
  |                           receives offer
  |                                  |
  |          TCP Connect + Session   |
  +--------------------------------> |
                                     |
                                gameplay loop
                               Hit / Stand / State
Layers
server/ → offer broadcasting + TCP accept loop + session management

client/ → UDP listener + TCP session handler + UI loop

common/ → protocol encode/decode + cards/deck utilities

📁 Project Structure
text
Copy code
blackijecky-Team51/
├─ client/        # Client entry + UDP listener + TCP session + terminal UI
├─ server/        # Server entry + offer broadcaster + TCP server + game sessions
├─ common/        # Shared protocol + cards logic
├─ tests/         # Unit/integration tests incl. edge cases
└─ README.md
✅ Requirements
Python 3.x

Recommended: venv

Tests: pytest

🚀 Quickstart
1) Clone
bash
Copy code
git clone https://github.com/BarMiyara/blackijecky-Team51.git
cd blackijecky-Team51
2) Create & activate venv
bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
3) Install dependencies
bash
Copy code
pip install pytest
▶️ Run
Server
bash
Copy code
python3 server/Server.py
Client (new terminal)
bash
Copy code
python3 client/client.py
🧪 Tests
Run all tests:

bash
Copy code
pytest -q
Verbose:

bash
Copy code
pytest -v
Run one file:

bash
Copy code
pytest -q tests/test_protocol.py
🧨 Reliability & Edge Cases
This project is tested against real-world networking failures:

✅ multiple clients / concurrency

✅ malformed requests / invalid decisions

✅ partial TCP reads (message split across reads)

✅ slow clients / timeouts

✅ invalid rounds values

✅ disconnect mid-round

🧯 Troubleshooting
“Imports fail / ModuleNotFoundError”
Run from repo root:

bash
Copy code
pwd
ls
You should see:

text
Copy code
client  common  server  tests  README.md
“Client can’t find offers”
UDP broadcast can be blocked on some networks.
Try running client & server on the same machine first.

“Client can’t connect”
Start the server first and check firewall/network permissions.

🧭 Roadmap (Nice-to-have)
 Add requirements.txt

 Add GitHub Actions CI (run pytest on every push/PR)

 Add a short protocol message table (opcode → meaning)

 Add demo screenshot/GIF under /assets

👥 Team
Bar Miyara — https://github.com/BarMiyara

Yuval Pariente — https://github.com/yuvalpariente

