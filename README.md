# crypto-price-mcp

An [MCP](https://modelcontextprotocol.io) server that gives AI agents **live crypto prices**.

An LLM's knowledge is frozen at training time, so it can't answer "what's the price of BTC right now?".
This gives an agent tools to fetch that live: current prices, the list of symbols, and recent candles.
It returns data only. It never suggests a trade or where the price is headed.

## Tools it gives an agent

| Tool | What it returns |
|---|---|
| `get_price(symbol)` | Current price of one coin, e.g. `BTC` |
| `get_prices(symbols)` | Current prices for several coins at once |
| `list_symbols()` | Every symbol it can price (200+) |
| `get_candles(symbol, interval, count)` | Recent OHLCV price history (1m … 1d) |

Data comes from the public [Hyperliquid](https://hyperliquid.xyz) API. The core fetching uses the
Python standard library only.

## Use with an MCP client (e.g. Claude Desktop)

```bash
pip install "crypto-price-mcp[mcp]"
```

Add it to your MCP client's config, for example:

```json
{
  "mcpServers": {
    "crypto-prices": {
      "command": "crypto-price-mcp"
    }
  }
}
```

Then your agent can answer "what's ETH trading at?" or "show me BTC's last 24 hours" by calling the
tools, instead of guessing from stale training data.

## Use from plain Python

```python
from crypto_price_mcp import prices

prices.get_price("BTC")          # {'symbol': 'BTC', 'price': 64980.5, 'as_of': ...}
prices.get_candles("ETH", "1h", 24)
prices.list_symbols()
```

## Tests

```bash
python -m unittest discover -s tests     # network is mocked, runs offline
```

## Note

This is a market-data source for agents. It reports prices; it does not give trading signals, predict
direction, or place orders.

## License

MIT.
