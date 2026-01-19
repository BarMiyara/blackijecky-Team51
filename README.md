<h1 align="center">🃏 BlackiJecky — Team51</h1>

<p align="center">
  <b>UDP Discovery</b> • <b>TCP Sessions</b> • <b>Shared Protocol</b> • <b>Edge-Case Tested</b>
</p>


<p align="center">
  Client–server Blackjack in Python — discover servers via <b>UDP offers</b>, play via <b>TCP sessions</b>, with a shared <b>protocol layer</b> and a tough test suite.
</p>


<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.x-blue" />
  <img alt="Networking" src="https://img.shields.io/badge/Networking-UDP%20%2B%20TCP-purple" />
  <img alt="Architecture" src="https://img.shields.io/badge/Architecture-client%20%7C%20server%20%7C%20common-success" />
  <img alt="Tests" src="https://img.shields.io/badge/Tests-pytest-brightgreen" />
  <img alt="Status" src="https://img.shields.io/badge/Status-stable-success" />
</p>


<p align="center">
  <a href="#-quick-run">Quick Run</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-project-structure">Structure</a> •
  <a href="#-tests">Tests</a> •
  <a href="#-troubleshooting">Troubleshooting</a>
</p>



<hr/>

<h2>🎬 Demo</h2>

<p align="center">
  <img src="assets/demo.mp4" alt="BlackiJecky demo" width="900" />
</p>
<p align="center">
  <i>UDP offer discovery → TCP session → terminal gameplay (Hit/Stand)</i>
</p>


<hr/>



<h2>⚡ Overview</h2>


<ul>
  <li>✅ <b>UDP discovery</b> — server broadcasts offers, clients auto-detect and join</li>
  <li>✅ <b>TCP sessions</b> — reliable gameplay communication per client</li>
  <li>✅ <b>Shared <code>common/</code> layer</b> — protocol + cards logic (single source of truth)</li>
  <li>✅ <b>Terminal UI</b> — clean rounds, hands, totals, and actions</li>
  <li>✅ <b>Hardcore testing</b> — malformed packets, partial reads, slow clients, disconnects, concurrency</li>
</ul>

<hr/>

<h2 id="-quick-run">🚀 Quick Run</h2>

```bash
python3 server/Server.py
python3 client/client.py
```
<hr/> <h2 id="-architecture">🧠 Architecture</h2> <h3>UDP → TCP Flow</h3>
    


The project is intentionally split into three layers:

- `server/` → networking + session orchestration
- `client/` → discovery + TCP session + UI
- `common/` → shared protocol + cards logic (used by both ends)

### 🔁 Communication Flow (UDP → TCP)
```text
         UDP Broadcast (Offer) 
Server  ----------------------->  Client
  |                                  |
  |                           picks offer
  |                                  |
  |          TCP Connect + Session   |
  +--------------------------------> |
                                     |
                                gameplay loop
                               Hit / Stand / State
```
<h3>Layers</h3> <ul> <li><code>server/</code> — offer broadcasting, TCP accept loop, session management</li> <li><code>client/</code> — UDP listener, TCP session handler, terminal UI</li> <li><code>common/</code> — shared protocol encode/decode + cards utilities</li> </ul> <hr/> <h2 id="-project-structure">📁 Project Structure</h2>

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

<hr/> <h2>✅ Requirements</h2> <ul> <li><b>Python 3.x</b></li> <li>Recommended: <b>venv</b></li> <li>Tests: <b>pytest</b></li> </ul> <hr/> <h2>🔧 Setup</h2>

```bash
git clone https://github.com/BarMiyara/blackijecky-Team51.git
cd blackijecky-Team51

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

pip install pytest

```

<hr/> <h2>▶️ Running the Project</h2> <h3>Run Server</h3>

```bash
python3 server/Server.py

```
<h3>Run Client (new terminal)</h3>

```bash
python3 client/client.py

```
<hr/> <h2 id="-tests">🧪 Tests</h2> <h3>Run everything</h3>

```bash
pytest -q

```
<h3>Verbose</h3>

```bash
pytest -v

```
<h3>Run a single file</h3>

```bash
pytest -q tests/test_protocol.py

```
<hr/> <h2>🧨 Edge Cases Covered</h2> <ul> <li>✅ multiple clients / concurrency</li> <li>✅ malformed requests</li> <li>✅ invalid player decisions</li> <li>✅ partial TCP reads (messages split across reads)</li> <li>✅ slow clients / timeouts</li> <li>✅ invalid round values</li> <li>✅ disconnect mid-round</li> </ul> <hr/> <h2>🔐 Protocol Layer</h2> <ul> <li><code>common/protocol.py</code> is the single source of truth for:</li> <li>encoding outgoing messages</li> <li>decoding incoming messages</li> <li>validating message structure + correctness</li> </ul> <p> Both client and server use it — no duplicated protocol logic. </p> <hr/> <h2 id="-troubleshooting">🧯 Troubleshooting</h2> <h3>Imports fail (<code>ModuleNotFoundError</code>)</h3> <p>Run from repo root:</p>

```bash
pwd
ls
```
<p>You should see:</p>

```text
client  common  server  tests  README.md
```

<h3>Client can’t find offers</h3> <p> UDP broadcast may be blocked on some networks. Try running server &amp; client on the same machine first. </p> <h3>Client can’t connect</h3> <p> Start the server first, then run the client. Check firewall/network restrictions if needed. </p> <hr/> <h2>🧭 Roadmap</h2> <ul> <li>[ ] Add <code>requirements.txt</code></li> <li>[ ] Add GitHub Actions CI (run <code>pytest</code> on push/PR)</li> <li>[ ] Add protocol message table (opcode → meaning)</li> <li>[ ] Add GIF demo (terminal gameplay)</li> </ul> <hr/> <h2>👥 Team</h2> <ul> <li><b>Bar Miyara</b> — https://github.com/BarMiyara</li> <li><b>Yuval Pariente</b> — https://github.com/yuvalpariente</li> </ul> <hr/> <h2 id="-license">📄 License</h2> <p>Educational project.</p> 


```

