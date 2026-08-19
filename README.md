![CI](https://github.com/realMNohgee/Poly_Watch/actions/workflows/ci.yml/badge.svg) ![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

# polywatch 🔍

**Polymarket wallet analyst, arbitrage scout, and bullshit detector.** Zero dependencies, pure Python stdlib.

> Part of the trading suite — verify profit claims before you copy-trade.

## One tool, many domains

| Domain | What polywatch does for you |
|---|---|
| 🕵️ **Due Diligence** | Verify any wallet's actual PnL — never trust a Twitter thread again |
| 💰 **Arbitrage** | Scan markets for UP+DOWN < $1.00 opportunities |
| 📊 **Market Research** | List top markets by volume, liquidity, category |
| 🤖 **Trading Bots** | Feed structured JSON to your bot for automated sniping |

## Install

```bash
git clone git@github.com:realMNohgee/Poly_Watch.git
cd Poly_Watch
python3 polywatch.py --help
```

Zero dependencies. Python 3.9+. No pip install.

## Quick start

```bash
# Verify someone's profit claims
python3 polywatch.py wallet 0x32ed2e546b187ca15e2841edc82b22c713cf8ec3

# Hunt for arbitrage
python3 polywatch.py scout

# Top crypto markets
python3 polywatch.py markets --category crypto --limit 10

# JSON output for your trading bot
python3 polywatch.py scout --format json
```

## Real example — bullshit detection

Actual output from a live run (`wallet` reads Polymarket's public Data API):

```console
$ python3 polywatch.py wallet 0x32ed2e546b187ca15e2841edc82b22c713cf8ec3

🔍 Wallet: 0x32ed2e546b187ca15e2841edc82b22c713cf8ec3
  Positions: 22
  Portfolio value: $1,693.22
  Cost basis: $1,323.16
  Unrealized PnL: $+370.05
  Realized PnL: $-322.96
  Win/Loss: 19W / 3L

  Verdict: 🟠 SMALL TIME — lunch money | 📈 Profitable

  Top positions:
    🟢 Bitcoin Up or Down on August 19?
       Size: 440 | Avg: 0.8945 | Now: 0.9995 | PnL: $+46.22
    🟢 Ethereum Up or Down on August 19?
       Size: 205 | Avg: 0.6924 | Now: 0.9995 | PnL: $+63.05
    🟢 Solana Up or Down on August 19?
       Size: 49 | Avg: 0.5600 | Now: 0.9950 | PnL: $+21.34
    ...
```

A wallet that looks impressive on Twitter might be pocket change on-chain. `polywatch` gives you the actual numbers.

> **Note:** `wallet`, `scout`, and `markets` hit Polymarket's live API, so the numbers change every minute. CI runs `py_compile` + `--help` offline so tests never depend on the network.

## License

MIT — see [LICENSE](LICENSE).

---

🧰 **[Tool on Hermtica Marketplace](https://hermtica.com/marketplace)** — the open, agent-agnostic marketplace for AI agent tools.
