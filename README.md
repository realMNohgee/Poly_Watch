# polywatch 🔍

**Polymarket wallet analyst, arbitrage scout, and bullshit detector.** Zero dependencies, pure Python stdlib.

> Part of the trading suite — verify profit claims before you copy-trade.

## One tool, many domains

| Domain | What polywatch does for you |
|---|---|
| 🕵️ **Due Diligence** | Verify any wallet's actual PnL — never trust a Twitter thread again |
| 💰 **Arbitrage** | Scan markets for UP+DOWN < $1.00 opportunities |
| 📊 **Market Research** | List top markets by volume, liquidity, category |
| 🤖 **Trading Bots** | Feed structured JSON to your bot for automated snipping |

## Install

```bash
git clone git@github.com:realMNohgee/Poly_Watch.git
cd Poly_Watch
python3 polywatch.py --help
```

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

## Example: Bullshit Detection

```
$ polywatch wallet 0x32ed2e546b187ca15e2841edc82b22c713cf8ec3

🔍 Wallet: 0x32ed2e546...
  Positions: 24
  Portfolio value: $646.74
  Verdict: 🔴 MICRO — pocket change | 📈 Profitable
```

Twitter said $20K → $160K. Reality: $600 portfolio. 😂

## License

MIT — see [LICENSE](LICENSE).

---

🧰 **[Tool on Hermtica Marketplace](https://hermtica.com/marketplace)** — the open, agent-agnostic marketplace for AI agent tools.
