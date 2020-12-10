import pandas
import webbrowser as browser
import robin_stocks as robinhood
from pandas_datareader import data as web
from datetime import datetime
from progressbar import ProgressBar, Bar, Percentage, ETA, FileTransferSpeed

from .get_indicators import getEMA, getRSI


def getRobinhoodSymbols():
    login = robinhood.login('phillipsloan24@gmail.com', '54bR&Srkm7EU')
    my_stocks = robinhood.build_holdings()
    return list(my_stocks.keys())


def printRobinhoodSymbols():
    print('\n----------------------------------- Robinhood Symbols -----------------------------------')
    login = robinhood.login('phillipsloan24@gmail.com', '54bR&Srkm7EU')
    my_stocks = robinhood.build_holdings()
    for ticker in my_stocks.keys():
        print(ticker)
