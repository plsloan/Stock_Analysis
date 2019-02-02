import time
import pandas
import requests
import datetime
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle, islice
from pandas_datareader import data as web
from progressbar import ProgressBar, Bar, Percentage, ETA, FileTransferSpeed

def main():
    # nasdaq_symbols = pandas.read_csv('Data/NASDAQ.csv')['Symbol']
    # nyse_symbols = pandas.read_csv('Data/NYSE.csv')['Symbol']
    my_symbols = ['RMD', 'LXRX', 'MPX', 'PER', 'GOLD', 'TRI', 'KEN', 'ET', 'LYG', 'MUFG', 'VIV', 'CNHI', 'BSBR']


    # dates
    today = datetime.datetime.now()
    start = today - datetime.timedelta(days=365)
    end = today

    # get data
    # getSuggestedNYSE(start, end, nyse_symbols)
    # today = datetime.datetime.now()
    # getSuggestedNASDAQ(start, end, nasdaq_symbols)
    getMySymbols(start, end, my_symbols)
    

# get stocks
def getSuggestedNYSE(start, end, symbols):
    current_index = 0
    widgets = [Bar(marker='=',left='[',right=']'), ' ', Percentage(), ' ', ETA(), ' ', FileTransferSpeed()]
    progress_bar = ProgressBar(widgets=widgets, maxval=2570)
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
def getSuggestedNASDAQ(start, end, symbols):
    current_index = 0
    widgets = [Bar(marker='=',left='[',right=']'), ' ', Percentage(), ' ', ETA(), ' ', FileTransferSpeed()]
    progress_bar = ProgressBar(widgets=widgets, maxval=3076)
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
def getMySymbols(start, end, symbols):
    current_index = 0
    widgets = [Bar(marker='=',left='[',right=']'), ' ', Percentage(), ' ', ETA(), ' ', FileTransferSpeed()]
    progress_bar = ProgressBar(widgets=widgets, maxval=3076)
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
    for stock in results:
        print(stock['Ticker'], stock['EMA - 50'], stock['EMA - 200'])#, stock['RSI'])

# calculate EMA
def getEMA(data, span):
    return data['Close'].ewm(span=span, min_periods=0, adjust=False, ignore_na=True).mean().iloc[-1]

# calculate RSI
def getRSI(data):
    series = data['Close']
    period = 14
    delta = series.diff().dropna()
    if (len(series) >= 14):
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
        u = u.drop(u.index[:(period-1)])
        d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
        d = d.drop(d.index[:(period-1)])
        rs = u.ewm(com=period-1, adjust=False).mean() / d.ewm(com=period-1, adjust=False).mean()
        return (100 - 100 / (1 + rs)).iloc[-1]
    else: 
        return 100


if __name__ == '__main__':
    main()