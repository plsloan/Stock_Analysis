import os
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
    scrape_MACD_crossover.main()
    update_crossover_prices.main()
    analyze_MACD.main()
    
    # replace with percentage analysis
    open_MACD_charts.main()
    scrape_symbol_list.main()
    update_watchlist_prices.main()
    analyze_watchlist.main()


    # # get data from stock exchanges
    # nasdaq_symbols = get_nasdaq_tickers()
    # nyse_symbols = get_nyse_tickers()
    # my_symbols = getRobinhoodSymbols()
    # macd_df = scrape_MACD_crossover.main()
    # macd_under25 = macd_df[macd_df['Close'] < 25]

    # decision = input('Fresh scrape? ')
    # if decision.lower()[0] == 'y':
    #     decision = input('Nasdaq, NYSE, or both? ')
    #     if decision.lower()[:2] == 'na':
    #         scrape_historical_data(nasdaq_symbols, 'nasdaq')
    #     elif decision.lower()[:2] == 'ny':
    #         scrape_historical_data(nyse_symbols, 'nyse')
    #     elif decision.lower()[0] == 'b':
    #         scrape_historical_data(nasdaq_symbols, 'nasdaq')
    #         scrape_historical_data(nyse_symbols, 'nyse')
    #     else: 
    #         exit("\nInvalid input...")
    # elif decision.lower()[0] == 'n':
    #     pass
    # else:
    #     exit("\nInvalid input...")

    # decision = input('Would you like to examine one stock or all available stocks? ')
    # if decision.lower()[0] == 'o':
    #     decision = 'y'
    #     while decision.lower()[0] == 'y':
    #         # get ticker
    #         ticker = input('\nEnter ticker: ')
    #         # get/convert days
    #         days = input('Over how many days: ')
    #         if days == '':
    #             days = 365
    #         else:
    #             days = int(days)
    #         # dates
    #         today = datetime.datetime.now()
    #         start = today - datetime.timedelta(days=days)
    #         end = today
    #         # get what to show
    #         show_data = input('Show data? (y/n) ').lower()
    #         show_analysis = input('Show analysis? (y/n) ').lower()
    #         show_plot = input('Show graph? (y/n) ').lower()
    #         # check path for file and import
    #         if os.path.exists('Data/NASDAQ/' + ticker.upper() + '.csv'):
    #             data = pandas.read_csv('Data/NASDAQ/' + ticker.upper() + '.csv', delimiter=', ', engine='python')
    #         elif os.path.exists('Data/NYSE/' + ticker.upper() + '.csv'):
    #             data = pandas.read_csv('Data/NYSE/' + ticker.upper() + '.csv', delimiter=', ', engine='python')
    #         else:
    #             data = web.DataReader(ticker, data_source='yahoo', start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
    #         # indicator calculations
    #         data['Boll. Upper'], data['Boll. Center'], data['Boll. Lower'] = getBollingerBand(data)     # upper & lower are a little off
    #         data['MACD'], data['Signal'] = getMACD(data)
    #         data['RSI'] = getRSI(data)
    #         data['EMA 50'] = getEMA(data, 50)
    #         data['EMA 200'] = getEMA(data, 200)                                                         # a little off
    #         # show stuff
    #         data_bool = False
    #         plot_bool = False
    #         analysis_bool = False
    #         if show_data == 'y':        data_bool = True
    #         if show_analysis == 'y':    analysis_bool = True
    #         if show_plot == 'y':        plot_bool = True
    #         if data_bool:       outputData(data, days=days)
    #         if analysis_bool:   outputAnalysis(data, ticker, days=days)
    #         if plot_bool:       browser.open('https://finance.yahoo.com/chart/' + ticker)
    #         # another?
    #         decision = input('\nAnalyze another stock (y/n)? ')
    # elif decision.lower()[0] == 'a':
    #     # get/convert days
    #     days = input('Over how many days: ')
    #     if days == '':
    #         days = 365
    #     else:
    #         days = int(days)
    #     # dates
    #     today = datetime.datetime.now()
    #     start = today - datetime.timedelta(days=days)
    #     end = today
    #     # get what to show
    #     show_data = input('Show data? (y/n) ').lower()
    #     show_analysis = input('Show analysis? (y/n) ').lower()
    #     # get Nasdaq
    #     progress_bar = progress_bar_mine(len(nasdaq_symbols) + len(nyse_symbols))
    #     progress_bar.start(label="Nasdaq Symbols")
    #     for i in range(len(nasdaq_symbols)):
    #         if os.path.exists('Data/NASDAQ/' + nasdaq_symbols[i].upper() + '.csv'):
    #             data = pandas.read_csv('Data/NASDAQ/' + nasdaq_symbols[i].upper() + '.csv', delimiter=', ', engine='python')
    #         elif os.path.exists('Data/NYSE/' + nasdaq_symbols[i].upper() + '.csv'):
    #             data = pandas.read_csv('Data/NYSE/' + nasdaq_symbols[i].upper() + '.csv', delimiter=', ', engine='python')
    #         else:
    #             data = web.DataReader(nasdaq_symbols[i], data_source='yahoo', start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
    #         if len(data['Close']) > 200:
    #             # indicator calculations
    #             data['Boll. Upper'], data['Boll. Center'], data['Boll. Lower'] = getBollingerBand(data)     # upper & lower are a little off
    #             data['MACD'], data['Signal'] = getMACD(data)
    #             data['RSI'] = getRSI(data)
    #             data['EMA 50'] = getEMA(data, 50)
    #             data['EMA 200'] = getEMA(data, 200)                                                         # a little off
    #             # show stuff
    #             data_bool = False
    #             analysis_bool = False
    #             if show_data == 'y':        data_bool = True
    #             if show_analysis == 'y':    analysis_bool = True
    #             if data_bool:       outputData(data, days=days)
    #             if analysis_bool:   outputAnalysis(data, nasdaq_symbols[i], days=days)
    #         progress_bar.update(i)
    #     # get NYSE
    #     for i in range(len(nyse_symbols)):
    #         if os.path.exists('Data/NASDAQ/' + nyse_symbols[i].upper() + '.csv'):
    #             data = pandas.read_csv('Data/NASDAQ/' + nyse_symbols[i].upper() + '.csv', delimiter=', ', engine='python')
    #         elif os.path.exists('Data/NYSE/' + nyse_symbols[i].upper() + '.csv'):
    #             data = pandas.read_csv('Data/NYSE/' + nyse_symbols[i].upper() + '.csv', delimiter=', ', engine='python')
    #         else:
    #             data = web.DataReader(nyse_symbols[i], data_source='yahoo', start=start.strftime('%m/%d/%Y'), end=end.strftime('%m/%d/%Y'))
    #         if len(data['Close']) > 200:
    #             # indicator calculations
    #             data['Boll. Upper'], data['Boll. Center'], data['Boll. Lower'] = getBollingerBand(data)     # upper & lower are a little off
    #             data['MACD'], data['Signal'] = getMACD(data)
    #             data['RSI'] = getRSI(data)
    #             data['EMA 50'] = getEMA(data, 50)
    #             data['EMA 200'] = getEMA(data, 200)                                                         # a little off
    #             # show stuff
    #             data_bool = False
    #             analysis_bool = False
    #             if show_data == 'y':        data_bool = True
    #             if show_analysis == 'y':    analysis_bool = True
    #             if data_bool:       outputData(data, days=days)
    #             if analysis_bool:   outputAnalysis(data, nyse_symbols[i], days=days)
    #         progress_bar.update(i + len(nasdaq_symbols))
    #     progress_bar.finish()

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
def outputAnalysis(data, ticker, days=0):
    print()
    print('---------- ' + ticker.upper() + ' Analysis ----------')

    # Bollinger Location: top / bottom
    boll_location = ''
    if data['Close'].iloc[-1] > data['Boll. Center'].iloc[-1]:
        print('Bollinger Location: Top half')
        boll_location = 'top'
    elif data['Close'].iloc[-1] < data['Boll. Center'].iloc[-1]:
        print('Bollinger Location: Bottom half')
        boll_location = 'bottom'

    # In Bollinger Bands: Yes / Overbought / Oversold / ?
    in_band = ''
    if (data['High'].iloc[-1] > data['Boll. Upper'].iloc[-1] and data['Low'].iloc[-1] < data['Boll. Lower'].iloc[-1]):
        print('In Bollinger Bands: Narrow bands or high volatility')
        in_band = '?'
    elif (data['High'].iloc[-1] > data['Boll. Upper'].iloc[-1]):
        print('In Bollinger Bands: No - overbought')
        in_band = 'overbought'
    elif (data['Low'].iloc[-1] < data['Boll. Lower'].iloc[-1]):
        print('In Bollinger Bands: No - oversold')
        in_band = 'oversold'
    else:
        print('In Bollinger Bands: Yes')
        in_band = 'yes'

    # MACD Location: Greater/Less/Equals(1/-1/0) than 0
    macd_location = ''
    if (data['MACD'].iloc[-1] > 0):
        print('MACD Location: Greater than 0')
        macd_location = '1'
    elif (data['MACD'].iloc[-1] < 0):
        print('MACD Location: Less than 0')
        macd_location = '-1'
    else:
        print('MACD Location: Equals 0')
        macd_location = '0'

    # Recent MACD Crossover: Buy/Sell/No
    recent_crossover = False
    if (data['MACD'].iloc[-1] > data['Signal'].iloc[-1]):
        for i in range(2, 6):
            if (data['MACD'].iloc[-1*i] <= data['Signal'].iloc[-1*i]):
                recent_crossover = True
        if (recent_crossover):
            print('Recent MACD Crossover: Yes - Buy')
            recent_crossover = 'buy'
        else: 
            print('Recent MACD Crossover: No')
            recent_crossover = 'no'
    else: 
        for i in range(2, 6):
            if (data['MACD'].iloc[-1*i] >= data['Signal'].iloc[-1*i]):
                recent_crossover = True
        if (recent_crossover):
            print('Recent MACD Crossover: Yes - Sell')
            recent_crossover = 'sell'
        else: 
            print('Recent MACD Crossover: No')
            recent_crossover = 'no'

    # EMA support: Yes/No
    ema_support = ''
    if (data['EMA 50'].iloc[-1] > data['EMA 200'].iloc[-1]):
        print('EMA Support: Yes')
        ema_support = 'yes'
    else:
        print('EMA Support: No')
        ema_support = 'no'

    # RSI: Normal/Overbought/Oversold
    if (data['RSI'].iloc[-1] >= 70):
        print('RSI: Overbought')
        rsi_support = 'overbought'
    elif (data['RSI'].iloc[-1] <= 30):
        print('RSI: Oversold')
        rsi_support = 'oversold'
    else:
        print('RSI: Normal')
        rsi_support = 'normal'

    # Udacity indicators
    if in_band == 'oversold' and macd_location == -1 and recent_crossover == 'no':
        print("Udacity: Check out this stock")
    else:
        print("Udacity: Nah fam")

    analysis = [boll_location, in_band, macd_location, recent_crossover, ema_support, rsi_support]
    score = getScore(analysis)
    if score >= 7:
        print('Advice: Buy')
    elif score < 7 and score > 3:
        print('Advice: Watch')
    else:
        print('Advice: Sell')
def getScore(analysis):
    # boll_location, in_band, macd_location, recent_crossover, ema_support, rsi_support
    score = 0
    if analysis[0].lower() == 'bottom':                     score = score + 1
    if analysis[1].lower() == 'yes':                        score = score + 1
    elif analysis[1].lower() == 'oversold':                 score = score + 2
    if analysis[2] == -1 and analysis[3].lower() == 'buy':  score = score + 4
    elif analysis[3].lower() == 'buy':                      score = score + 2
    if analysis[4].lower() == 'yes':                        score = score + 1
    if analysis[5].lower() == 'oversold':                   score = score + 3
    elif analysis[5].lower() == 'normal':                   score = score + 2  
    return score    


# -------------- MAIN ------------- #

if (__name__ == '__main__'):
    main()