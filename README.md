# 🃏 BlackiJecky — Team51
### UDP Discovery • TCP Sessions • Protocol-Driven Blackjack • Hardcore Test Suite

**Client–server Blackjack in Python**  
Server discovery via **UDP offers**, gameplay over **TCP sessions**, shared **protocol layer**, and **aggressive edge-case testing**.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Networking](https://img.shields.io/badge/Networking-UDP%20Discovery%20%2B%20TCP%20Sessions-purple)
![Architecture](https://img.shields.io/badge/Architecture-Client%20%7C%20Server%20%7C%20Common-success)
![Tests](https://img.shields.io/badge/Tests-pytest-brightgreen)
![Status](https://img.shields.io/badge/Status-Stable-success)

---

## 🎬 Demo
> Drop a screenshot/GIF here to instantly make the repo look premium.

![Demo](assets/demo.png)

---

## 📌 Table of Contents
- [⚡ Overview](#-overview)
- [🧠 Architecture](#-architecture)
- [📁 Project Structure](#-project-structure)
- [✅ Requirements](#-requirements)
- [🚀 Quickstart](#-quickstart)
- [▶️ Running the Project](#️-running-the-project)
- [🕹️ Gameplay](#️-gameplay)
- [🧪 Tests](#-tests)
- [🧨 Edge Cases Covered](#-edge-cases-covered)
- [🔐 Protocol Layer](#-protocol-layer)
- [🧯 Troubleshooting](#-troubleshooting)
- [🧭 Roadmap](#-roadmap)
- [👥 Team](#-team)
- [📄 License](#-license)

---

## ⚡ Overview
**BlackiJecky** is a Python **client–server Blackjack** project built like a real networking app:

- ✅ **UDP Discovery** — server broadcasts offers, clients auto-detect and join  
- ✅ **TCP Sessions** — reliable gameplay communication per session  
- ✅ **Shared `common/` layer** — one source of truth for protocol + cards  
- ✅ **Terminal UI** — clean rounds, hands, totals, and actions  
- ✅ **Hardcore tests** — nasty real-world networking edge cases included  

If it passes the tests — it’s not just “working”… it’s **solid**.

---

## 🧠 Architecture

### UDP → TCP Flow
```text
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
```
Layers
server/ → offer broadcasting, TCP accept loop, session management

client/ → UDP listener, TCP session handler, terminal UI

common/ → shared protocol encode/decode + cards utilities

📁 Project Structure
```text
blackijecky-Team51/
├─ README.md
├─ client/
│  ├─ client.py              # Main client entry
│  ├─ udp_listener.py        # Listens to server offers (UDP)
│  ├─ tcp_session.py         # TCP gameplay session
│  └─ ui.py                  # Terminal UI
├─ common/
│  ├─ protocol.py            # Shared protocol: encode/decode/validation
│  └─ cards.py               # Cards / deck logic
├─ server/
│  ├─ Server.py              # Main server entry
│  ├─ Offer_Broadcaster.py   # Sends UDP offers
│  ├─ Tcp_Server.py          # TCP server implementation
│  └─ Game_Session.py        # Game session orchestration
└─ tests/
   ├─ helpers.py
   ├─ test_cards.py
   ├─ test_protocol.py
   ├─ test_tcp_smoke.py
   ├─ test_concurrency.py
   ├─ test_malformed_request.py
   ├─ test_edge_partial_request.py
   ├─ test_edge_slow_client.py
   ├─ test_edge_invalid_rounds.py
   ├─ test_edge_invalid_decision.py
   └─ test_edge_disconnect_midround.py
```

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
2) Setup virtual environment
bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
3) Install dependencies
bash
Copy code
pip install pytest
▶️ Running the Project
Run Server
bash
Copy code
python3 server/Server.py
Run Client (new terminal)
bash
Copy code
python3 client/client.py
🕹️ Gameplay
The terminal UI shows:

Dealer hand

Your hand

Totals + round counter

Wins / losses / ties

Actions:

Hit

Stand

🧪 Tests
Run everything:

bash
Copy code
pytest -q
Verbose:

bash
Copy code
pytest -v
Run a single file:

bash
Copy code
pytest -q tests/test_protocol.py
🧨 Edge Cases Covered
The test suite is designed to catch real-world networking failures:

✅ multiple clients / concurrency

✅ malformed requests

✅ invalid player decisions

✅ partial TCP reads (messages split across reads)

✅ slow clients / timeouts

✅ invalid round values

✅ disconnect mid-round

🔐 Protocol Layer
The stability comes from one shared source of truth:

common/protocol.py handles encode/decode

validates structure + correctness

prevents duplicated logic between client and server

🧯 Troubleshooting
Imports fail (ModuleNotFoundError)
Run from repo root:

bash
Copy code
pwd
ls
You should see:

text
Copy code
client  common  server  tests  README.md
Client can’t find offers
UDP broadcast may be blocked on some networks.
Try running server & client on the same machine first.

Client can’t connect
Start the server first, then run the client.
Check firewall/network restrictions if needed.

🧭 Roadmap
 Add requirements.txt

 Add GitHub Actions CI (run pytest on push/PR)

 Add protocol message table (opcode → meaning)

 Add GIF demo (terminal gameplay)

👥 Team
Bar Miyara — https://github.com/BarMiyara

Yuval Pariente — https://github.com/yuvalpariente

📄 License
Educational project.

makefile
Copy code
::contentReference[oaicite:0]{index=0}
