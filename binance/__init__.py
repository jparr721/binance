import os
from typing import Final, List

BINANCE_CODE_DIR = os.path.dirname(os.path.abspath(__file__))

BINANCE_DATA_HEADER: Final[List[str]] = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_asset_volume",
    "number_of_trades",
    "taker_buy_base_asset_volume",
    "taker_buy_quote_asset_volume",
    "ignore",
]

# List of token pairs to fetch data for; these are the pairs currently
# in my dune dashboard to start out
TOKEN_PAIRS: Final[List[str]] = ["ETHUSDC", "ETHUSDT", "ETHDAI"]

# Use the nosync path for cloud providers on local machines. This prevents it from exploding personal storage.
BINANCE_DATA_DIR: Final[str] = "data.nosync"
BINANCE_COMBINED_DATA_DIR: Final[str] = os.path.join(BINANCE_DATA_DIR, "combined")
