from binance_historical_data import BinanceDataDumper
import pandas as pd
import os

# NOTE: can install binance_historical_data library with "pip install binance-historical-data"
# current directory should be "binance data" to run the code properly

# list of token pairs to fetch data for; these are the pairs currently in my dune dashboard to start out
pairs = ['ETHUSDC', 'ETHUSDT', 'ETHDAI']

# download the monthly data (and daily data for the current month) for the listed pairs
# i.e. k-line data at 1-minute intervals, as Milionis et al. used close prices at the end of each minute
data_dumper = BinanceDataDumper('data')
data_dumper.dump_data(tickers=pairs)

for pair in pairs:
    # path to CSV that will contain all the data for this pair combined across months
    # no header row, but column names are:
    # Open time,Open,High,Low,Close,Volume,Close time,Quote asset volume,Number of trades,Taker buy base asset volume,Taker buy quote asset volume,Ignore
    # as specified here: https://github.com/binance/binance-public-data#klines
    combo_csv_path = 'data/combo CSVs/' + pair + '-1m-all.csv'
    combo_csv = open(combo_csv_path, 'w')

    # path to folders containing monthly data for this pair
    folder_path = data_dumper.get_local_dir_to_data(pair, 'monthly')

    # list of monthly files for this pair
    flist = os.listdir(folder_path)
    flist.sort()

    # put each month's data into combo CSV
    for fname in flist:
        df = pd.read_csv(folder_path + '/' + fname, header=None)
        df.to_csv(combo_csv_path, mode='a', header=None, index=False)

    # list of daily files
    d_folder_path = data_dumper.get_local_dir_to_data(pair, 'daily')
    d_flist = os.listdir(d_folder_path)
    d_flist.sort()

    # put daily data into combo CSV
    for fname in d_flist:
        df = pd.read_csv(d_folder_path + '/' + fname, header=None)
        df.to_csv(combo_csv_path, mode='a', header=None, index=False)

    combo_csv.close()
