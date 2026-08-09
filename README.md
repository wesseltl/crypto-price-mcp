<!-- mcp-name: io.github.wesseltl/price-data-mcp -->

# price-data-mcp

![PyPI](https://img.shields.io/pypi/v/hyperliquid-price-mcp)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![MCP](https://img.shields.io/badge/MCP-server-6E56CF)
![License](https://img.shields.io/badge/license-MIT-green)
![Deps](https://img.shields.io/badge/core-zero%20dependencies-lightgrey)

**Give your AI agent live market prices.** An [MCP](https://modelcontextprotocol.io) server that lets
an agent look up the current price, the full symbol list, and recent price history for 200+ coins.

An LLM's knowledge is frozen at training time, so it can't answer *"what's BTC trading at right now?"*.
This closes that gap. It returns market data only. It never gives a trading signal or predicts direction.

## What your agent can do with it

> **You:** What's Bitcoin trading at, and how has it moved over the last few hours?
>
> **Agent** *(calls `get_price("BTC")` and `get_candles("BTC", "1h", 6)`)*:
> Bitcoin is at **$65,047**. Over the last 6 hours it's held between $65,020 and $65,132 on rising volume.

The agent fetches real numbers instead of guessing from stale training data.

## Quickstart

```bash
pip install "hyperliquid-price-mcp[mcp]"
```

Add it to your MCP client (e.g. Claude Desktop's config):

```json
{
  "mcpServers": {
    "market-prices": { "command": "hyperliquid-price-mcp" }
  }
}
```

Restart your client. The agent now has four tools.

## The tools

| Tool | Returns |
|---|---|
| `get_price("BTC")` | `{"symbol": "BTC", "price": 65047.5, "as_of": 1786204330859}` |
| `get_prices(["BTC","ETH"])` | current price for each, missing ones flagged |
| `list_symbols()` | every symbol it can price (200+) |
| `get_candles("BTC","1h",100)` | recent OHLCV history (`1m` … `1d`) |

Example candle:
```json
{"open_ms": 1786201200000, "open": 65104.0, "high": 65132.0,
 "low": 65020.0, "close": 65047.0, "volume": 409.43, "trades": 7014}
```

## Also usable from plain Python

```python
from price_data_mcp import prices

prices.get_price("BTC")                # {'symbol': 'BTC', 'price': 65047.5, 'as_of': ...}
prices.get_candles("ETH", "1h", 24)    # last 24 hourly candles
prices.list_symbols()                  # ['AAVE', 'ADA', 'APE', ...]
```

## How it works

Prices come from the public [Hyperliquid](https://hyperliquid.xyz) info API. The core fetching module
(`price_data_mcp/prices.py`) uses the **Python standard library only** (no dependencies), so it's
small and easy to audit. The `mcp` extra is only needed to run the server.

## Tests

```bash
python -m unittest discover -s tests     # network is mocked, runs fully offline
```

## Scope

A market-data source for agents. It reports prices and history. It does **not** give trading signals,
predict where the price is going, or place orders.

## License

MIT
