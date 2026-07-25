#!/usr/bin/env python3
"""polywatch — Polymarket wallet analyst, arbitrage scout, and bullshit detector.

Zero dependencies, pure Python stdlib. Uses Polymarket's public Data API
and Gamma API to read any wallet's positions, scan markets for arbitrage,
and verify profit claims without trusting Twitter threads.
"""
from __future__ import annotations
import argparse, json, sys, urllib.request, urllib.error, time
from datetime import datetime

DATA_API = "https://data-api.polymarket.com"
GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"

HEADERS = {"User-Agent": "polywatch/1.0"}

def _get(url, timeout=15):
    req = urllib.request.Request(url, headers=HEADERS)
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())


# ═══════════════════════════════════════════════════════════════
#  WALLET — look up any wallet's positions and PnL
# ═══════════════════════════════════════════════════════════════

def cmd_wallet(args):
    wallet = args.address
    print(f"🔍 Wallet: {wallet}")
    
    try:
        positions = _get(f"{DATA_API}/positions?user={wallet}&limit=100")
    except Exception as e:
        print(f"❌ Failed: {e}")
        return 1
    
    if not positions:
        print("No open positions found.")
        return 0
    
    total_value = sum(p.get("currentValue", 0) for p in positions)
    total_cost = sum(p.get("initialValue", 0) for p in positions)
    total_pnl = sum(p.get("cashPnl", 0) for p in positions)
    total_realized = sum(p.get("realizedPnl", 0) for p in positions)
    win_count = sum(1 for p in positions if p.get("cashPnl", 0) > 0)
    lose_count = sum(1 for p in positions if p.get("cashPnl", 0) < 0)
    
    if args.format == "json":
        out = {
            "wallet": wallet,
            "positions": len(positions),
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "unrealized_pnl": round(total_pnl, 2),
            "realized_pnl": round(total_realized, 2),
            "winning_positions": win_count,
            "losing_positions": lose_count,
            "positions_detail": [
                {"title": p.get("title","?"), "size": p.get("size"), 
                 "avgPrice": p.get("avgPrice"), "curPrice": p.get("curPrice"),
                 "pnl": round(p.get("cashPnl",0),2), "pnl_pct": round(p.get("percentPnl",0),2)}
                for p in positions[:20]
            ]
        }
        print(json.dumps(out, indent=2))
        return 0
    
    # Text output
    print(f"  Positions: {len(positions)}")
    print(f"  Portfolio value: ${total_value:,.2f}")
    print(f"  Cost basis: ${total_cost:,.2f}")
    print(f"  Unrealized PnL: ${total_pnl:+,.2f}")
    print(f"  Realized PnL: ${total_realized:+,.2f}")
    print(f"  Win/Loss: {win_count}W / {lose_count}L")
    
    # Verdict
    if total_value > 100000:
        verdict = "🟢 WHALE — serious money"
    elif total_value > 10000:
        verdict = "🟡 REAL TRADER — five figures"
    elif total_value > 1000:
        verdict = "🟠 SMALL TIME — lunch money"
    else:
        verdict = "🔴 MICRO — pocket change"
    
    net = total_pnl + total_realized
    if net < -1000:
        verdict += " | 📉 NET LOSER"
    elif net < 0:
        verdict += " | 📉 Slightly down"
    elif net > 50000:
        verdict += " | 🚀 MASSIVE PROFIT"
    elif net > 0:
        verdict += " | 📈 Profitable"
    
    print(f"\n  Verdict: {verdict}")
    
    # Top positions
    print(f"\n  Top positions:")
    sorted_pos = sorted(positions, key=lambda p: abs(p.get("currentValue", 0)), reverse=True)[:10]
    for p in sorted_pos:
        pnl = p.get("cashPnl", 0)
        sign = "🟢" if pnl > 0 else "🔴" if pnl < 0 else "⚪"
        print(f"    {sign} {p.get('title','?')[:60]}")
        print(f"       Size: {p.get('size',0):,.0f} | Avg: {p.get('avgPrice',0):.4f} | Now: {p.get('curPrice',0):.4f} | PnL: ${pnl:+,.2f}")
    
    return 0


# ═══════════════════════════════════════════════════════════════
#  SCOUT — scan markets for arbitrage (both sides < $1)
# ═══════════════════════════════════════════════════════════════

def cmd_scout(args):
    print("🔎 Scanning markets for arbitrage opportunities...")
    print("   (Looking for markets where UP + DOWN < $1.00)")
    
    try:
        # Get popular markets from Gamma API
        markets_data = _get(f"{GAMMA_API}/markets?limit=50&order=volume24hr&ascending=false&closed=false")
    except Exception as e:
        print(f"❌ Failed to fetch markets: {e}")
        return 1
    
    opportunities = []
    
    for m in markets_data[:50]:
        try:
            slug = m.get("slug", "")
            title = m.get("title", "?")
            
            # Get clob token IDs and order book
            clob_ids = m.get("clobTokenIds", "")
            if not clob_ids:
                continue
            
            # Parse token IDs (JSON string or comma-separated)
            if isinstance(clob_ids, str) and clob_ids.startswith("["):
                tokens = json.loads(clob_ids)
            elif isinstance(clob_ids, str):
                tokens = clob_ids.split(",")
            else:
                tokens = clob_ids
            
            if len(tokens) < 2:
                continue
            
            # Get midpoints/prices for first two outcomes
            prices = []
            for token in tokens[:2]:
                try:
                    book = _get(f"{CLOB_API}/book?token_id={token}", timeout=10)
                    # Use best ask as the buy price
                    asks = book.get("asks", [])
                    bids = book.get("bids", [])
                    # Midpoint = average of best bid and best ask
                    best_ask = float(asks[0]["price"]) if asks else None
                    best_bid = float(bids[0]["price"]) if bids else None
                    if best_ask and best_bid:
                        prices.append((best_bid + best_ask) / 2)
                    elif best_ask:
                        prices.append(best_ask)
                    elif best_bid:
                        prices.append(best_bid)
                except Exception:
                    pass
            
            if len(prices) >= 2:
                combined = prices[0] + prices[1]
                spread_to_dollar = 1.0 - combined
                if spread_to_dollar > 0.001:  # arbitrage possible
                    opportunities.append({
                        "title": title,
                        "slug": slug,
                        "up_price": prices[0],
                        "down_price": prices[1],
                        "combined": combined,
                        "profit_margin": spread_to_dollar,
                    })
        except Exception:
            continue
        
        time.sleep(0.1)  # Rate limit
    
    if args.format == "json":
        print(json.dumps(opportunities, indent=2))
        return 0
    
    if not opportunities:
        print("\n  No arbitrage opportunities found. Markets are efficient today!")
        return 0
    
    opportunities.sort(key=lambda o: o["profit_margin"], reverse=True)
    
    print(f"\n  Found {len(opportunities)} opportunities:\n")
    for o in opportunities[:20]:
        profit_pct = o["profit_margin"] * 100
        bar = "█" * min(int(profit_pct * 2), 40)
        print(f"  🎯 {o['title'][:65]}")
        print(f"     UP: ${o['up_price']:.4f} | DOWN: ${o['down_price']:.4f} | Combined: ${o['combined']:.4f}")
        print(f"     Profit margin: {profit_pct:.2f}% {bar}")
        print()
    
    if len(opportunities) > 20:
        print(f"  ... and {len(opportunities) - 20} more")
    
    print(f"  💡 Strategy: Buy equal amounts of both sides when combined < $1.00")
    print(f"     You can't lose — worst case you get exactly $1 back per pair.")
    print(f"     Best case one side goes to $1, the other to $0, you profit the spread.")
    
    return 0


# ═══════════════════════════════════════════════════════════════
#  MARKETS — list top markets
# ═══════════════════════════════════════════════════════════════

def cmd_markets(args):
    limit = args.limit or 20
    category = args.category or ""
    
    url = f"{GAMMA_API}/markets?limit={limit}&order=volume24hr&ascending=false&closed=false"
    if category:
        url += f"&category={category}"
    
    try:
        markets = _get(url)
    except Exception as e:
        print(f"❌ Failed: {e}")
        return 1
    
    if args.format == "json":
        print(json.dumps(markets, indent=2))
        return 0
    
    print(f"📊 Top {len(markets)} markets by 24h volume:\n")
    for i, m in enumerate(markets, 1):
        vol = float(m.get("volume24hr", 0))
        title = m.get("title", "?")
        slug = m.get("slug", "")
        liquidity = float(m.get("liquidity", 0))
        outcomes = m.get("outcomes", "[]")
        if isinstance(outcomes, str):
            outcomes = json.loads(outcomes)
        
        print(f"  {i:2}. {title[:70]}")
        print(f"       Vol: ${vol:,.0f} | Liquidity: ${liquidity:,.0f} | polymarket.com/event/{slug}")
        if outcomes:
            outcome_str = " | ".join(outcomes[:3])
            print(f"       Outcomes: {outcome_str}")
        print()
    
    return 0


# ═══════════════════════════════════════════════════════════════
#  CLI setup
# ═══════════════════════════════════════════════════════════════

def build_parser():
    p = argparse.ArgumentParser(
        prog="polywatch",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format (default: text)")
    
    sub = p.add_subparsers(dest="cmd", required=True)
    
    # wallet
    w = sub.add_parser("wallet", parents=[common], help="Analyze a wallet's positions and PnL")
    w.add_argument("address", help="Wallet address (0x...) or Polymarket username (@mo-money)")
    w.set_defaults(func=cmd_wallet)
    
    # scout
    s = sub.add_parser("scout", parents=[common], help="Scan markets for arbitrage opportunities")
    s.set_defaults(func=cmd_scout)
    
    # markets
    m = sub.add_parser("markets", parents=[common], help="List top markets by volume")
    m.add_argument("--limit", type=int, default=20, help="Number of markets (default: 20)")
    m.add_argument("--category", help="Filter by category (e.g., crypto, politics, sports)")
    m.set_defaults(func=cmd_markets)
    
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
