# 🃏 BlackiJecky — Team51  
### UDP Discovery • TCP Sessions • Protocol-Driven Blackjack • Hardcore Test Suite

<div align="center">

**A clean client–server Blackjack implementation in Python**  
Built with UDP server discovery, TCP gameplay sessions, a shared protocol layer, and a serious edge-case test suite.

<br/>

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Architecture](https://img.shields.io/badge/Architecture-client%20%7C%20server%20%7C%20common-success)
![Networking](https://img.shields.io/badge/Networking-UDP%20discovery%20%2B%20TCP%20sessions-purple)
![Tests](https://img.shields.io/badge/Tests-pytest%20%7C%20edge%20cases-brightgreen)

</div>

---

## ⚡ What is this?
**BlackiJecky** is a Python **client–server Blackjack** project built around real networking patterns:

- ✅ **UDP discovery** — server broadcasts game offers  
- ✅ **TCP sessions** — reliable gameplay communication  
- ✅ **Shared protocol layer** — single source of truth under `common/`  
- ✅ **Terminal UX** — clear round stats + cards rendering + simple actions  
- ✅ **Edge-case tested** — partial reads, malformed packets, timeouts, disconnects, concurrency  

If it passes the test suite — it’s not just “working”… it’s **robust**.

---

## 🧠 Architecture

### Communication Flow (UDP → TCP)
```text
         UDP Broadcast (Offer)
Server  ----------------------->  Client
  |                                  |
  |                           detects offer
  |                                  |
  |          TCP Connect + Session   |
  +--------------------------------> |
                                     |
                                gameplay loop
                               Hit / Stand / State
                               
