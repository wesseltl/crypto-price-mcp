"""Tests for the price logic. Network calls are mocked so tests run offline / in CI."""
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto_price_mcp import prices

FAKE_MIDS = {"BTC": "65000.5", "ETH": "1920.0", "SOL": "74.25"}
FAKE_META = {"universe": [{"name": "ETH"}, {"name": "BTC"}, {"name": "SOL"}]}
FAKE_CANDLES = [
    {"t": 1000, "o": "100", "h": "110", "l": "95", "c": "105", "v": "12.5", "n": 42},
    {"t": 2000, "o": "105", "h": "120", "l": "104", "c": "118", "v": "8.0", "n": 30},
]


class TestPrices(unittest.TestCase):
    @patch("crypto_price_mcp.prices._post", return_value=FAKE_MIDS)
    def test_get_price(self, _):
        r = prices.get_price("btc")
        self.assertEqual(r["symbol"], "BTC")
        self.assertEqual(r["price"], 65000.5)
        self.assertIn("as_of", r)

    @patch("crypto_price_mcp.prices._post", return_value=FAKE_MIDS)
    def test_get_price_unknown_raises(self, _):
        with self.assertRaises(ValueError):
            prices.get_price("DOGECOINZ")

    @patch("crypto_price_mcp.prices._post", return_value=FAKE_MIDS)
    def test_get_prices_marks_missing(self, _):
        out = prices.get_prices(["BTC", "NOPE"])
        by = {r["symbol"]: r for r in out}
        self.assertTrue(by["BTC"]["found"])
        self.assertFalse(by["NOPE"]["found"])
        self.assertIsNone(by["NOPE"]["price"])

    @patch("crypto_price_mcp.prices._post", return_value=FAKE_META)
    def test_list_symbols_sorted(self, _):
        self.assertEqual(prices.list_symbols(), ["BTC", "ETH", "SOL"])

    @patch("crypto_price_mcp.prices._post", return_value=FAKE_CANDLES)
    def test_get_candles(self, _):
        c = prices.get_candles("BTC", "1h", 2)
        self.assertEqual(len(c), 2)
        self.assertEqual(c[0]["open"], 100.0)
        self.assertEqual(c[1]["close"], 118.0)
        self.assertEqual(c[0]["trades"], 42)

    def test_get_candles_bad_interval(self):
        with self.assertRaises(ValueError):
            prices.get_candles("BTC", "3s")


if __name__ == "__main__":
    unittest.main()
