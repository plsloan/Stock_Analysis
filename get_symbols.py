import time
import pandas
import requests
import datetime
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle, islice
from pandas_datareader import data as web
from progressbar import ProgressBar, Bar, Percentage, ETA, FileTransferSpeed

from get_indicators import getEMA, getRSI

def getSuggestedNYSE(start, end, symbols):
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
def getSuggestedNASDAQ(start, end, symbols):
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
def getSuggestedSymbols(start, end, symbols):
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
def printSuggestedNYSE(start, end, symbols):
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
def printSuggestedNASDAQ(start, end, symbols):
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
def printSuggestedSymbols(start, end, symbols):
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
    for stock in results:
        print(stock['Ticker'], stock['EMA - 50'], stock['EMA - 200'])#, stock['RSI'])