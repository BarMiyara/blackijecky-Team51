
# 🃏 BlackiJecky — Team51
### UDP Discovery • TCP Sessions • Shared Protocol • Hardcore Test Suite

<div align="center">

**Client–server Blackjack in Python**  
Server discovery via **UDP offers**, gameplay over **TCP sessions**, shared **protocol layer**, and **aggressive edge-case testing**.

<br/>

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Networking](https://img.shields.io/badge/Networking-UDP%20Discovery%20%2B%20TCP%20Sessions-purple)
![Architecture](https://img.shields.io/badge/Architecture-Client%20%7C%20Server%20%7C%20Common-success)
![Tests](https://img.shields.io/badge/Tests-pytest-brightgreen)
![Status](https://img.shields.io/badge/Status-Stable-success)

</div>

---

## 🎬 Demo
> Add a screenshot/GIF to instantly make the repository look premium.

![Demo](assets/demo.png)

---

## 📌 Table of Contents
- [⚡ Overview](#-overview)
- [🧠 Architecture](#-architecture)
- [📁 Project Structure](#-project-structure)
- [✅ Requirements](#-requirements)
- [🚀 Quickstart](#-quickstart)
- [▶️ Running the Project](#️-running-the-project)
- [🧪 Tests](#-tests)
- [🧨 Edge Cases Covered](#-edge-cases-covered)
- [🧯 Troubleshooting](#-troubleshooting)
- [🧭 Roadmap](#-roadmap)
- [👥 Team](#-team)
- [📄 License](#-license)

---

## ⚡ Overview
**BlackiJecky** is a Python **client–server Blackjack** project designed like a real networking application:

✅ **UDP Discovery** — the server broadcasts offers and clients can auto-detect them  
✅ **TCP Sessions** — reliable communication for gameplay per session  
✅ **Shared `common/` layer** — one source of truth for protocol + cards  
✅ **Terminal UI** — clear rounds, hands, totals, and actions  
✅ **Serious tests** — validates correctness + nasty real-world networking edge cases  

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

Layers

server/ → offer broadcasting, TCP accept loop, session management

client/ → UDP listener, TCP session handler, terminal UI

common/ → shared protocol encode/decode + cards utilities

📁 Project Structure
blackijecky-Team51/
├─ README.md
├─ client/
│  ├─ client.py              # Main client entry
│  ├─ udp_listener.py        # Listens to server offers (UDP)
│  ├─ tcp_session.py         # TCP gameplay session
│  └─ ui.py                  # Terminal UI
├─ common/
│  ├─ protocol.py            # Shared protocol: encode/decode/validation
│  └─ cards.py               # Deck/cards logic
├─ server/
│  ├─ Server.py              # Main server entry
│  ├─ Offer_Broadcaster.py   # Sends UDP offers
│  ├─ Tcp_Server.py          # TCP server implementation
│  └─ Game_Session.py        # Blackjack game session logic
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

✅ Requirements

Python 3.x

Recommended: venv

Tests: pytest

🚀 Quickstart
1) Clone
git clone https://github.com/BarMiyara/blackijecky-Team51.git
cd blackijecky-Team51

2) Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

3) Install dependencies
pip install pytest

▶️ Running the Project
Run Server
python3 server/Server.py

Run Client (new terminal)
python3 client/client.py

🧪 Tests

Run everything:

pytest -q


Verbose:

pytest -v


Run a single file:

pytest -q tests/test_protocol.py

🧨 Edge Cases Covered

This suite is designed to catch real-world networking issues:

✅ multiple clients / concurrency

✅ malformed requests

✅ invalid user decisions

✅ partial TCP reads (message split across reads)

✅ slow clients / timeouts

✅ invalid round values

✅ disconnect mid-round

Passing this suite means your implementation handles more than just the “happy path”.

🧯 Troubleshooting
Imports fail (ModuleNotFoundError)

Make sure you're in the repo root:

pwd
ls


You should see:

client  common  server  tests  README.md

Client can’t find offers

UDP broadcast may be blocked on some networks.
Try running client & server on the same machine first.

Client can’t connect

Start the server first, then run the client.
Also check firewall/network restrictions.

🧭 Roadmap

 Add requirements.txt

 Add GitHub Actions CI (run pytest on every push/PR)

 Add protocol message table (opcode → meaning)

 Add GIF demo (terminal gameplay)

👥 Team

Bar Miyara — https://github.com/BarMiyara

Yuval Pariente — https://github.com/yuvalpariente

📄 License

Educational project.
