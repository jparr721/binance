from typing import Final, List

BINANCE_DATA_HEADER: Final[List[str]] = [
    "Open time",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "Close time",
    "Quote asset volume",
    "Number of trades",
    "Taker buy base asset volume",
    "Taker buy quote asset volume",
    "Ignore",
]

# List of token pairs to fetch data for; these are the pairs currently
# in my dune dashboard to start out
TOKEN_PAIRS: Final[List[str]] = ["ETHUSDC", "ETHUSDT", "ETHDAI"]
