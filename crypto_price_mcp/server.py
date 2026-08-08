"""server.py — expose live crypto prices as MCP tools that any AI agent can call.

An LLM's knowledge is frozen at training time, so it can't answer "what's the price of BTC right now?".
This server gives an agent tools to fetch that live: current prices, the list of symbols, and recent
candles. It returns data only; it never suggests a trade or a direction.

Run:  python -m crypto_price_mcp.server        (needs:  pip install "crypto-price-mcp[mcp]")

Point your MCP client (Claude Desktop, or any MCP client) at that command.
"""
from __future__ import annotations

from crypto_price_mcp import prices

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "The MCP server needs the 'mcp' package. Install it with:\n"
        '    pip install "crypto-price-mcp[mcp]"'
    ) from exc

mcp = FastMCP("crypto-prices")


@mcp.tool()
def get_price(symbol: str) -> dict:
    """Get the current price of a crypto asset.

    Args:
        symbol: the coin ticker, e.g. "BTC", "ETH", "SOL".
    Returns the symbol, its current price (USD), and an as-of timestamp (ms).
    """
    return prices.get_price(symbol)


@mcp.tool()
def get_prices(symbols: list[str]) -> list[dict]:
    """Get current prices for several crypto assets at once.

    Args:
        symbols: list of tickers, e.g. ["BTC", "ETH", "SOL"].
    """
    return prices.get_prices(symbols)


@mcp.tool()
def list_symbols() -> list[str]:
    """List all crypto symbols this server can price."""
    return prices.list_symbols()


@mcp.tool()
def get_candles(symbol: str, interval: str = "1h", count: int = 100) -> list[dict]:
    """Get recent OHLCV candles (price history) for a crypto asset.

    Args:
        symbol: the coin ticker, e.g. "BTC".
        interval: one of 1m, 5m, 15m, 1h, 4h, 1d.
        count: how many recent candles to return (default 100).
    Returns candles oldest-first, each with open/high/low/close/volume.
    """
    return prices.get_candles(symbol, interval, count)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
