import pandas 
import webbrowser as browser
import robin_stocks as robinhood
from pandas_datareader import data as web
from datetime import datetime
from progressbar import ProgressBar, Bar, Percentage, ETA, FileTransferSpeed

from get_indicators import getEMA, getRSI

now = datetime.now().strftime('%Y-%m-%d')

def get_nasdaq_tickers():
    return pandas.read_csv('Data/NASDAQ/_NASDAQ.csv')['Symbol']
def get_nyse_tickers():
    return pandas.read_csv('Data/NYSE/_NYSE.csv')['Symbol']
def getSuggestedNYSE(start, end):
    symbols = pandas.read_csv('Data/NYSE.csv')['Symbol']
    current_index = 0
    results = []
    for ticker in symbols:
        data = web.DataReader(ticker, data_source='yahoo', start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
        if getEMA(data, 50) > getEMA(data, 200) and getRSI(data) < 30:
            results.append({
                'Ticker' : ticker, 
                'EMA - 50' : getEMA(data, 50), 
                'EMA - 200' : getEMA(data, 200), 
                'RSI' : getRSI(data)})
        current_index = current_index + 1
    stocks = []
    for stock in results:
        stocks.append([stock['Ticker'], stock['EMA - 50'], stock['EMA - 200'], stock['RSI']])
    return stocks
def printSuggestedNYSE(start, end):
    symbols = pandas.read_csv('Data/NYSE.csv')['Symbol']
    current_index = 0
    widgets = [Bar(marker='=',left='[',right=']'), ' ', Percentage(), ' ', ETA(), ' ', FileTransferSpeed()]
    progress_bar = ProgressBar(widgets=widgets, maxval=len(symbols))
    results = []

    print('\n--------------------------------- NYSE Symbols ---------------------------------')
    progress_bar.start()
    for ticker in symbols:
        data = web.DataReader(ticker, data_source='yahoo', start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
        if getEMA(data, 50) > getEMA(data, 200) and getRSI(data) < 30:
            results.append({
                'Ticker' : ticker, 
                'EMA - 50' : getEMA(data, 50), 
                'EMA - 200' : getEMA(data, 200), 
                'RSI' : getRSI(data)})
        current_index = current_index + 1
        progress_bar.update(current_index)
    progress_bar.finish()
    for stock in results:
        print(stock['Ticker'], stock['EMA - 50'], stock['EMA - 200'], stock['RSI'])
def getSuggestedNASDAQ(start, end):
    symbols = pandas.read_csv('Data/NASDAQ.csv')['Symbol']
    current_index = 0
    results = []
    for ticker in symbols:
        data = web.DataReader(ticker, data_source='yahoo', start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
        if getEMA(data, 50) > getEMA(data, 200) and getRSI(data) < 30:
            results.append({
                'Ticker' : ticker, 
                'EMA - 50' : getEMA(data, 50), 
                'EMA - 200' : getEMA(data, 200), 
                'RSI' : getRSI(data)})
        current_index = current_index + 1
    stocks = []
    for stock in results:
        stocks.append([stock['Ticker'], stock['EMA - 50'], stock['EMA - 200'], stock['RSI']])
    return stocks
def printSuggestedNASDAQ(start, end):
    symbols = pandas.read_csv('Data/NASDAQ.csv')['Symbol']
    current_index = 0
    widgets = [Bar(marker='=',left='[',right=']'), ' ', Percentage(), ' ', ETA(), ' ', FileTransferSpeed()]
    progress_bar = ProgressBar(widgets=widgets, maxval=len(symbols))
    results = []
    
    print('\n--------------------------------- NASDAQ Symbols --------------------------------')
    progress_bar.start()
    for ticker in symbols:
        data = web.DataReader(ticker, data_source='yahoo', start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
        if getEMA(data, 50) > getEMA(data, 200) and getRSI(data) < 30:
            results.append({
                'Ticker' : ticker, 
                'EMA - 50' : getEMA(data, 50), 
                'EMA - 200' : getEMA(data, 200), 
                'RSI' : getRSI(data)})
        current_index = current_index + 1
        progress_bar.update(current_index)
    progress_bar.finish()
    for stock in results:
        print(stock['Ticker'], stock['EMA - 50'], stock['EMA - 200'], stock['RSI'])
def getSuggestedSymbols(start, end, symbols):
    # symbols = ['RMD', 'LXRX', 'MPX', 'PER', 'GOLD', 'TRI', 'KEN', 'ET', 'LYG', 'MUFG', 'VIV', 'CNHI', 'BSBR']
    current_index = 0
    results = []
    for ticker in symbols:
        data = web.DataReader(ticker, data_source='yahoo', start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
        if getEMA(data, 50) > getEMA(data, 200): # and getRSI(data) < 30:
            results.append({
                'Ticker' : ticker, 
                'EMA - 50' : getEMA(data, 50), 
                'EMA - 200' : getEMA(data, 200)})#, 
                #'RSI' : getRSI(data)})
        current_index = current_index + 1
    stocks = []
    for stock in results:
        stocks.append([stock['Ticker'], stock['EMA - 50'], stock['EMA - 200']])#, stock['RSI'])
    return stocks
def printSuggestedSymbols(start, end, symbols):
    # symbols = ['RMD', 'LXRX', 'MPX', 'PER', 'GOLD', 'TRI', 'KEN', 'ET', 'LYG', 'MUFG', 'VIV', 'CNHI', 'BSBR']
    current_index = 0
    widgets = [Bar(marker='=',left='[',right=']'), ' ', Percentage(), ' ', ETA(), ' ', FileTransferSpeed()]
    progress_bar = ProgressBar(widgets=widgets, maxval=len(symbols))
    results = []

    print('\n----------------------------------- My Symbols ----------------------------------')
    progress_bar.start()
    for ticker in symbols:
        data = web.DataReader(ticker, data_source='yahoo', start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
        if getEMA(data, 50) > getEMA(data, 200): # and getRSI(data) < 30:
            results.append({
                'Ticker' : ticker, 
                'EMA - 50' : getEMA(data, 50), 
                'EMA - 200' : getEMA(data, 200)})#, 
                #'RSI' : getRSI(data)})
        current_index = current_index + 1
        progress_bar.update(current_index)
    progress_bar.finish()
    print()
    for stock in results:
        print(stock['Ticker'], stock['EMA - 50'], stock['EMA - 200'])#, stock['RSI'])
    input('\nPress Enter to exit...')
def getRobinhoodSymbols():
    login = robinhood.login('phillipsloan24@gmail.com','54bR&Srkm7EU')
    my_stocks = robinhood.build_holdings()
    return list(my_stocks.keys())
def printRobinhoodSymbols():
    print('\n----------------------------------- Robinhood Symbols -----------------------------------')
    login = robinhood.login('phillipsloan24@gmail.com','54bR&Srkm7EU')
    my_stocks = robinhood.build_holdings()
    for ticker in my_stocks.keys():
        print(ticker)
def getWatchlistSymbols(date=now):
    path = 'Data/Watchlist/'
    filename = path + date + '.csv'
    return pandas.read_csv(filename)['Symbol']
