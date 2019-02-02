import pandas
import datetime
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle, islice
from pandas_datareader import data as web

def main():
    print()

    # get data from stock exchanges
    # nasdaq_symbols = pandas.read_csv('Data/NASDAQ.csv')['Symbol']
    # nyse_symbols = pandas.read_csv('Data/NYSE.csv')['Symbol']

    # user input
    ticker = input('Enter ticker to examine: ')
    days = int(input('Over how many days: '))
    show_data = input('Show data? (y/n) ').lower()
    show_analysis = input('Show analysis? (y/n) ').lower()

    # dates
    today = datetime.datetime.now()
    start = today - datetime.timedelta(days=days)
    end = today

    # get data
    data = web.DataReader(ticker, data_source='yahoo', start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
    analysis = ''

    # indicator calculations
    data['Boll. Upper'], data['Boll. Center'], data['Boll. Lower'] = getBollingerBand(data)     # upper & lower are a little off
    data['MACD'], data['Signal'] = getMACD(data)
    data['RSI'] = getRSI(data)
    data['EMA 50'] = getEMA(data, 50)
    data['EMA 200'] = getEMA(data, 200)                                                         # a little off
    
    # show stuff
    data_bool = False
    plot_bool = False
    analysis_bool = False
    advice_bool = False

    if show_data == 'y':
        data_bool = True

    if show_analysis == 'y':
        show_advice = input('Show advice? (y/n) ').lower()
        analysis_bool = True
        if show_advice == 'y':
            advice_bool = True
    
    show_plot = input('Show graph? (y/n) ').lower()
    if show_plot == 'y':
        plot_bool = True
        
    if data_bool: outputData(data, days=days)
    if analysis_bool: analysis = outputAnalysis(data, days=days)
    if advice_bool: outputAdvice(data, analysis, days=days) 
    if plot_bool: showPlot(data, days=days)


# ---------- USED IN MAIN ---------- #

# calculate EMA
def getEMA(data, span):
    return data['Close'].ewm(span=span, min_periods=0, adjust=False, ignore_na=True).mean()

# calculate Bollinger Band data
def getBollingerBand(data):
    s = 20  # span
    x = 2   # standard deviation periods

    data_bollinger = data['Close'].ewm(span=s, min_periods=0, adjust=False, ignore_na=True)
    
    center = data_bollinger.mean()
    upper = data_bollinger.mean() + data_bollinger.std() * x
    lower = data_bollinger.mean() - data_bollinger.std() * x
    
    return upper, center, lower

# calculate MACD
def getMACD(data):
    macd = getEMA(data, 12) - getEMA(data, 26)
    sig  = macd.ewm(span=9, min_periods=0, adjust=False, ignore_na=True).mean()
    
    return macd, sig

# calculate RSI
def getRSI(data):
    series = data['Close']
    period = 14
    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
    d = d.drop(d.index[:(period-1)])
    rs = u.ewm(com=period-1, adjust=False).mean() / d.ewm(com=period-1, adjust=False).mean()
    return 100 - 100 / (1 + rs)

# shows plot for price info, MACD, and RSI
def showPlot(data, days=0):
    data_graph1 = data[['Close', 'Boll. Upper', 'Boll. Center', 'Boll. Lower', 'EMA 50', 'EMA 200']]
    data_graph2 = data[['MACD', 'Signal']]
    data_graph3 = data['RSI']
    
    labels1 = ['Close', 'Boll. Upper', 'Boll. Center', 'Boll. Lower', 'EMA 50', 'EMA 200']
    colors1 = ['k', 'r', 'orange', 'r', 'b', 'g']
    line_widths1 = ['2', '2', '1', '2', '0.5', '0.5']
    labels2 = ['MACD', 'Signal']
    colors2 = ['b', 'orange']
    line_widths2 = ['1', '1']

    if days == 0:
        plt.subplot(3, 1, 1)
        ax = plt.plot(data_graph1.iloc[-31:-1],)
    elif days > 0:
        plt.subplot(3, 1, 1)
        ax = plt.plot(data_graph1.iloc[(-1*days - 1):-1])
    else:
        print('Invalid day parameter')

    for i, l in enumerate(ax):
        plt.setp(l, linewidth=line_widths1[i], color=colors1[i], label=labels1[i])


    plt.legend(loc='upper left', fontsize='x-small')
    plt.ylabel('Closing Price')
    plt.title('Stock Information')
    

    if days == 0:
        plt.subplot(3, 1, 2)
        bx = plt.plot(data_graph2.iloc[-31:-1])
    elif days > 0:
        plt.subplot(3, 1, 2)
        bx = plt.plot(data_graph2.iloc[(-1*days - 1):-1])
    else:
        print('Invalid day parameter')

    for i, l in enumerate(bx):
        plt.setp(l, linewidth=line_widths2[i], color=colors2[i], label=labels2[i])
    
    plt.legend(loc='upper left', fontsize='x-small')
    plt.ylabel('MACD')
    plt.axhline(0, color='k', linewidth='0.4')

    if days == 0:
        plt.subplot(3, 1, 3)
        bx = plt.plot(data_graph3.iloc[-31:-1])
    elif days > 0:
        plt.subplot(3, 1, 3)
        bx = plt.plot(data_graph3.iloc[(-1*days - 1):-1])
    else:
        print('Invalid day parameter')

    plt.legend(loc='upper left', fontsize='x-small')
    plt.ylabel('RSI')
    plt.axhline(70, color='k', linewidth='0.4')
    plt.axhline(30, color='k', linewidth='0.4')
    plt.show()

# prints all data
def outputData(data, days=0):
    if (days == 0):
        print()
        print(data.tail())
        print()
    elif (days > 0):
        print()
        print(data.iloc[(-1*days - 1):-1])
        print()
    else: 
        print()
        print('Invalid day parameter')
        print()

# prints analysis and returns values
def outputAnalysis(data, days=0):
    print()
    print('---------- Analysis ----------')

    # Bollinger Location: Above/Below/On center
    boll_location = ''
    if (data['Close'][-1] > data['Boll. Center'][-1]):
        print('Bollinger Location: Top half')
        boll_location = 'top'
    elif (data['Close'][-1] < data['Boll. Center'][-1]):
        print('Bollinger Location: Bottom half')
        boll_location = 'bottom'
    else:
        pass

    # In Bollinger Bands: Yes / Overbought / Oversold
    in_band = ''
    if (data['High'][-1] > data['Boll. Upper'][-1] and data['Low'][-1] < data['Boll. Lower'][-1]):
        print('In Bollinger Bands: Narrow bands or high volatility')
        in_band = '?'
    elif (data['High'][-1] > data['Boll. Upper'][-1]):
        print('In Bollinger Bands: No - overbought')
        in_band = 'overbought'
    elif (data['Low'][-1] < data['Boll. Lower'][-1]):
        print('In Bollinger Bands: No - oversold')
        in_band = 'oversold'
    else:
        print('In Bollinger Bands: Yes')
        in_band = 'yes'

    # MACD Location: Greater/Less than 0
    macd_location = ''
    if (data['MACD'][-1] > 0):
        print('MACD Location: Greater than 0')
        macd_location = '1'
    elif (data['MACD'][-1] < 0):
        print('MACD Location: Less than 0')
        macd_location = '-1'
    else:
        print('MACD Location: Equals 0')
        macd_location = '0'

    # Recent MACD Crossover: Yes/No
    recent_crossover = False
    if (data['MACD'][-1] > data['Signal'][-1]):
        for i in range(2, 6):
            if (data['MACD'][-1*i] <= data['Signal'][-1*i]):
                recent_crossover = True
        if (recent_crossover):
            print('Recent MACD Crossover: Yes - Buy')
            recent_crossover = 'buy'
        else: 
            print('Recent MACD Crossover: No')
            recent_crossover = 'no'
    else: 
        for i in range(2, 6):
            if (data['MACD'][-1*i] >= data['Signal'][-1*i]):
                recent_crossover = True
        if (recent_crossover):
            print('Recent MACD Crossover: Yes - Sell')
            recent_crossover = 'sell'
        else: 
            print('Recent MACD Crossover: No')
            recent_crossover = 'no'

    # EMA support: Yes/No
    ema_support = ''
    if (data['EMA 50'][-1] > data['EMA 200'][-1]):
        print('EMA Support: Yes')
        ema_support = 'yes'
    else:
        print('EMA Support: No')
        ema_support = 'no'

    # RSI: Normal/Overbought/Oversold
    if (data['RSI'][-1] >= 70):
        print('RSI: Overbought')
        rsi_support = 'overbought'
    elif (data['RSI'][-1] <= 30):
        print('RSI: Oversold')
        rsi_support = 'oversold'
    else:
        print('RSI: Normal')
        rsi_support = 'normal'

    return [boll_location, in_band, macd_location, recent_crossover, ema_support, rsi_support]

# description here
def outputAdvice(data, analysis, days=0):
    # analysis
    # boll_location, in_band, macd_location, recent_crossover, ema_support, rsi_support
    print()    
    print('----------- Advice -----------')
    

    pass
    


# -------------- MAIN ------------- #

if (__name__ == '__main__'):
    main()