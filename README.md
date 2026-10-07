![CI](https://github.com/realMNohgee/Poly_Watch/actions/workflows/smoke.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)

# polywatch 🔍

**Polymarket wallet analyst, arbitrage scout, and bullshit detector — zero dependencies, pure Python stdlib.**

`polywatch` reads Polymarket's public **Data**, **Gamma**, and **CLOB** APIs so you can verify any wallet's real PnL, scan markets for UP+DOWN < $1.00 arbitrage, and list top markets by volume — all from one file with no `pip install`.

## Install

```bash
git clone git@github.com:realMNohgee/Poly_Watch.git
cd Poly_Watch
python3 polywatch.py --help
```

Requires only **Python 3.8+**. Zero third-party packages.

## Commands

### `--help`

```console
$ python3 polywatch.py --help
usage: polywatch [-h] {wallet,scout,markets} ...

polywatch — Polymarket wallet analyst, arbitrage scout, and bullshit detector.

Zero dependencies, pure Python stdlib. Uses Polymarket's public Data API
and Gamma API to read any wallet's positions, scan markets for arbitrage,
and verify profit claims without trusting Twitter threads.

positional arguments:
  {wallet,scout,markets}
    wallet              Analyze a wallet's positions and PnL
    scout               Scan markets for arbitrage opportunities
    markets             List top markets by volume

optional arguments:
  -h, --help            show this help message and exit
```

### `wallet` — verify a wallet's real PnL

Reads `/positions` from Polymarket's Data API and grades the account.

```console
$ python3 polywatch.py wallet 0x32ed2e546b187ca15e2841edc82b22c713cf8ec3
🔍 Wallet: 0x32ed2e546b187ca15e2841edc82b22c713cf8ec3
  Positions: 13
  Portfolio value: $435.74
  Cost basis: $788.26
  Unrealized PnL: $-352.53
  Realized PnL: $+128.59
  Win/Loss: 6W / 7L

  Verdict: 🔴 MICRO — pocket change | 📉 Slightly down

  Top positions:
    🟢 Bitcoin Up or Down - October 7, 12:00PM-4:00PM ET
       Size: 210 | Avg: 0.5476 | Now: 0.5850 | PnL: $+7.84
    🟢 Bitcoin Up or Down on October 8?
       Size: 200 | Avg: 0.4600 | Now: 0.5350 | PnL: $+15.00
    🔴 Ethereum Up or Down - October 7, 12:00PM-4:00PM ET
       Size: 100 | Avg: 0.8300 | Now: 0.7100 | PnL: $-12.00
    🟢 Bitcoin Up or Down - October 7, 2:05PM-2:10PM ET
       Size: 69 | Avg: 0.5693 | Now: 0.9750 | PnL: $+27.96
    🟢 Ethereum Up or Down - October 7, 12:00PM-4:00PM ET
       Size: 100 | Avg: 0.0900 | Now: 0.2900 | PnL: $+20.00
    🔴 Bitcoin Up or Down - October 7, 2:05PM-2:10PM ET
       Size: 607 | Avg: 0.4662 | Now: 0.0250 | PnL: $-267.77
    🔴 BNB Up or Down - October 7, 2PM ET
       Size: 19 | Avg: 0.8300 | Now: 0.6850 | PnL: $-2.75
    🟢 BNB Up or Down - October 7, 1PM ET
       Size: 8 | Avg: 0.8900 | Now: 0.9995 | PnL: $+0.84
    🟢 Solana Up or Down on October 8?
       Size: 3 | Avg: 0.4500 | Now: 0.4800 | PnL: $+0.10
    🔴 Solana Up or Down - October 7, 2PM ET
       Size: 4 | Avg: 0.4000 | Now: 0.2450 | PnL: $-0.55
```

Machine-readable variant for bots — `--format json`:

```console
$ python3 polywatch.py wallet 0x32ed2e546b187ca15e2841edc82b22c713cf8ec3 --format json
🔍 Wallet: 0x32ed2e546b187ca15e2841edc82b22c713cf8ec3
{
  "wallet": "0x32ed2e546b187ca15e2841edc82b22c713cf8ec3",
  "positions": 10,
  "total_value": 925.94,
  "total_cost": 1009.49,
  "unrealized_pnl": -83.56,
  "realized_pnl": -137.97,
  "winning_positions": 5,
  "losing_positions": 5,
  "positions_detail": [
    {
      "title": "Bitcoin Up or Down - October 7, 2:05PM-2:10PM ET",
      "size": 676.676,
      "avgPrice": 0.939,
      "curPrice": 0.995,
      "pnl": 37.88,
      "pnl_pct": 5.96
    },
    {
      "title": "Bitcoin Up or Down - October 7, 12:00PM-4:00PM ET",
      "size": 210.0866,
      "avgPrice": 0.5476,
      "curPrice": 0.58,
      "pnl": 6.79,
      ...
```

### `scout` — hunt arbitrage (UP + DOWN < $1.00)

Pulls the 50 highest-volume open markets from Gamma, then reads each market's CLOB order book and flags pairs whose combined mid-price is under a dollar.

```console
$ python3 polywatch.py scout
🔎 Scanning markets for arbitrage opportunities...
   (Looking for markets where UP + DOWN < $1.00)

  No arbitrage opportunities found. Markets are efficient today!
```

When nothing is mispriced it says so; on a hit it prints the two sides, the combined price, and a profit-margin bar. JSON form (`scout --format json`) emits a JSON array — here, legitimately empty because no spread was live:

```console
$ python3 polywatch.py scout --format json
🔎 Scanning markets for arbitrage opportunities...
   (Looking for markets where UP + DOWN < $1.00)
[]
```

### `markets` — top markets by volume

```console
$ python3 polywatch.py markets --limit 5
📊 Top 5 markets by 24h volume:

   1. ?
       Vol: $2,642,175 | Liquidity: $1,850,969 | polymarket.com/event/cs2-prv-navi-2026-10-07
       Outcomes: PARIVISION | Natus Vincere

   2. ?
       Vol: $886,164 | Liquidity: $426,198 | polymarket.com/event/will-raphael-warnock-win-the-2028-democratic-presidential-nomination-914
       Outcomes: Yes | No

   3. ?
       Vol: $691,315 | Liquidity: $288,432 | polymarket.com/event/will-chris-van-hollen-win-the-2028-democratic-presidential-nomination
       Outcomes: Yes | No

   4. ?
       Vol: $638,219 | Liquidity: $635,242 | polymarket.com/event/putin-out-before-2027-346
       Outcomes: Yes | No

   5. ?
       Vol: $441,552 | Liquidity: $111,831 | polymarket.com/event/us-announces-end-of-iranian-blockade-by-october-15-2026
       Outcomes: Yes | No
```

> **Note:** Polymarket's `/markets?order=volume24hr` response intermittently omits the `title` field, so the label above shows `?` while slug, volume, liquidity, and outcomes are accurate. Do not trust a number just because it rendered.

## Real example — bullshit detection

A wallet that looks impressive on Twitter might be pocket change on-chain. The `wallet` command above returns `🔴 MICRO — pocket change | 📉 Slightly down` for an account down $352.53 unrealized — the exact numbers a hype thread leaves out. `polywatch` gives you the raw figures instead of the narrative.

## How it works

| Subcommand | API used | Endpoint |
|---|---|---|
| `wallet` | Data API | `GET https://data-api.polymarket.com/positions?user=<addr>` |
| `scout` | Gamma + CLOB | `GET /markets` then `GET /book?token_id=<id>` per outcome |
| `markets` | Gamma API | `GET https://gamma-api.polymarket.com/markets?order=volume24hr` |

All output is `text` by default; pass `--format json` for structured data.

## CI

Every push and PR runs `.github/workflows/smoke.yml`: a byte-compile gate plus `--help` for the top-level CLI and each subcommand, all offline, with `set -euo pipefail` so any non-zero exit fails the build. The functional subcommands hit live Polymarket APIs, so CI verifies CLI wiring without making network calls.

## License

MIT — see [LICENSE](LICENSE).

---

🧰 **[Tool on Hermtica Marketplace](https://hermtica.com/marketplace)**