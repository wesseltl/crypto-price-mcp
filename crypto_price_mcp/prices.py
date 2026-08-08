"""prices.py — fetch live crypto prices and candles. Standard library only (urllib).

Data comes from the public Hyperliquid info API. This module just fetches and returns it in a clean
shape; it says nothing about whether to buy, sell, or where the price is headed. It's a data source,
not trading advice.
"""
from __future__ import annotations

import json
import time
import urllib.request

API_URL = "https://api.hyperliquid.xyz/info"

INTERVAL_MS = {
    "1m": 60_000, "5m": 300_000, "15m": 900_000, "1h": 3_600_000,
    "4h": 14_400_000, "1d": 86_400_000,
}


def _post(body: dict, timeout: int = 15):
    req = urllib.request.Request(
        API_URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def all_mids() -> dict[str, float]:
    """Current mid price for every listed coin, as {symbol: price}."""
    return {k: float(v) for k, v in _post({"type": "allMids"}).items()}


def get_price(symbol: str) -> dict:
    """Current price for one symbol, e.g. get_price('BTC')."""
    symbol = symbol.upper()
    mids = all_mids()
    if symbol not in mids:
        raise ValueError(f"unknown symbol {symbol!r}")
    return {"symbol": symbol, "price": mids[symbol], "as_of": int(time.time() * 1000)}


def get_prices(symbols: list[str]) -> list[dict]:
    """Current prices for several symbols at once."""
    mids = all_mids()
    out = []
    for s in symbols:
        s = s.upper()
        out.append({"symbol": s, "price": mids.get(s), "found": s in mids})
    return out


def list_symbols() -> list[str]:
    """All tradable symbols currently listed."""
    meta = _post({"type": "meta"})
    return sorted(c["name"] for c in meta.get("universe", []))


def get_candles(symbol: str, interval: str = "1h", count: int = 100) -> list[dict]:
    """Recent OHLCV candles for a symbol. Returns oldest-first."""
    symbol = symbol.upper()
    if interval not in INTERVAL_MS:
        raise ValueError(f"unknown interval {interval!r}; use one of {list(INTERVAL_MS)}")
    per = INTERVAL_MS[interval]
    end = int(time.time() * 1000)
    start = end - count * per
    raw = _post({"type": "candleSnapshot",
                 "req": {"coin": symbol, "interval": interval, "startTime": start, "endTime": end}})
    return [{
        "open_ms": int(c["t"]), "open": float(c["o"]), "high": float(c["h"]),
        "low": float(c["l"]), "close": float(c["c"]), "volume": float(c["v"]), "trades": int(c["n"]),
    } for c in raw]
