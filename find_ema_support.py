import time
import pandas
import requests
import datetime
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle, islice
from pandas_datareader import data as web
from progressbar import ProgressBar, Bar, Percentage, ETA, FileTransferSpeed

from get_symbols import getSuggestedNASDAQ, getSuggestedNYSE, getSuggestedSymbols, printSuggestedNASDAQ, printSuggestedNYSE, printSuggestedSymbols
import scrape_MACD_crossover 

def main():
    # nasdaq_symbols = pandas.read_csv('Data/NASDAQ.csv')['Symbol']
    # nyse_symbols = pandas.read_csv('Data/NYSE.csv')['Symbol']
    # my_symbols = ['RMD', 'LXRX', 'MPX', 'PER', 'GOLD', 'TRI', 'KEN', 'ET', 'LYG', 'MUFG', 'VIV', 'CNHI', 'BSBR']
    macd_df = scrape_MACD_crossover.main()
    macd_under25 = macd_df[macd_df['Close'] < 25]

    # dates
    today = datetime.datetime.now()
    start = today - datetime.timedelta(days=365)
    end = today

    printSuggestedSymbols(start, end, macd_under25['Symbol'])
    return getSuggestedSymbols(start, end, macd_under25['Symbol'])



if __name__ == '__main__':
    main()