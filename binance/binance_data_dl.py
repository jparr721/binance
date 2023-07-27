import os

import pandas as pd
from binance_historical_data import BinanceDataDumper
from rich import print
from rich.progress import track

from binance import *


def download_binance_data(refresh: bool = False):
    # download the monthly data (and daily data for the current month) for the listed pairs
    # i.e. k-line data at 1-minute intervals, as Milionis et al. used close prices at the end of each minute
    data_dumper = BinanceDataDumper(BINANCE_DATA_DIR)
    if not os.path.exists(BINANCE_DATA_DIR) or refresh:
        data_dumper.dump_data(tickers=TOKEN_PAIRS)

    for pair in track(TOKEN_PAIRS, description="Filtering data into folders..."):
        # Make sure that the combined directory exists
        if not os.path.exists(BINANCE_COMBINED_DATA_DIR):
            print(f"[red]Directory {BINANCE_COMBINED_DATA_DIR} not found, creating")
            os.makedirs(BINANCE_COMBINED_DATA_DIR)

        # path to CSV that will contain all the data for this pair combined across months
        # no header row, but column names are:
        # Open time,Open,High,Low,Close,Volume,Close time,Quote asset volume,Number of trades,Taker buy base asset volume,Taker buy quote asset volume,Ignore
        # as specified here: https://github.com/binance/binance-public-data#klines
        combo_csv_path = os.path.join(BINANCE_COMBINED_DATA_DIR, pair + "-1m-all.csv")
        with open(combo_csv_path, "w+") as combo_csv:
            # Dump the headers
            combo_csv.write(",".join(BINANCE_DATA_HEADER) + "\n")

            # path to folders containing monthly data for this pair
            folder_path = data_dumper.get_local_dir_to_data(pair, "monthly")

            # list of monthly files for this pair
            flist = os.listdir(folder_path)
            flist.sort()

            # put each month's data into combo CSV
            for fname in flist:
                df = pd.read_csv(os.path.join(folder_path, fname), header=None)
                df.to_csv(combo_csv_path, mode="a", index=False, header=None)

            # list of daily files
            d_folder_path = data_dumper.get_local_dir_to_data(pair, "daily")
            d_flist = os.listdir(d_folder_path)
            d_flist.sort()

            # put daily data into combo CSV
            for fname in d_flist:
                df = pd.read_csv(os.path.join(d_folder_path, fname), header=None)
                df.to_csv(combo_csv_path, mode="a", index=False, header=None)
