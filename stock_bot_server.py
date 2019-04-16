import os
import glob
import pandas
import datetime
import warnings
from sys import exit
import webbrowser as browser
import matplotlib.pyplot as plt
from pandas_datareader import data as web

from progressbar_mine import progress_bar_mine
from scrape_exchange import scrape_historical_data
from get_indicators import getBollingerBand, getMACD, getRSI, getEMA
from get_symbols import getRobinhoodSymbols, get_nasdaq_tickers, get_nyse_tickers
# warnings.simplefilter("ignore")

import scrape_MACD_crossover, update_crossover_prices
import open_MACD_charts
import scrape_symbol_list, update_watchlist_prices
import analyze_MACD, analyze_watchlist


def main():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    scrape_MACD_crossover.main()
    if datetime.datetime.now().hour in [12, 15]:
        update_crossover_prices.main()

    # if today + '.csv' in glob.glob('Data/MACD_Crossover/'):
    #     crossover_csv = 'Data/MACD_Crossover/' + today + '.csv'
    #     tickers_MACD = pandas.read_csv(crossover_csv)['Symbol']
    
    # replace with percentage analysis
    # if not os.path.exists('Data/Watchlist/' + today + '.csv'):
    #     open_MACD_charts.main(already_scraped=True)
    
    while True:
        if datetime.datetime.now().hour >= 8 and datetime.datetime.now().hour < 18:
            scrape_symbol_list.main()#tickers=tickers)
            if datetime.datetime.now().minute in [0, 30]:
                print('\nUpdating ' + datetime.datetime.now().strftime('%H') + ':' + datetime.datetime.now().strftime('%M') + '...')
                update_watchlist_prices.main(continuous=True)


# -------------- MAIN ------------- #

if (__name__ == '__main__'):
    main()