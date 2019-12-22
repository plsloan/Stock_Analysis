from datetime import datetime
from db_connect import db
from db_utils import *
from my_enums import Exchange
from utils import get_command, strip_string
import textwrap


def main():
    if db.Stocks.count_documents({}) == 0:
        initialize_stocks()

    commands = textwrap.dedent('''
    Commands
    --------
     * delete stocks - delete all stock
     * delete records - delete all stock records
     * update records - update stock records
     * print stocks - prints stocks from a given exchange
     * get suggestions - prints all
     * cls - clears terminal
     * help - prints available commands
    ''')

    print(commands)

    # TODO: Move this to a service... type... thing
    # function maybe?
    user_input = get_command()
    while user_input != 'exit':
        if user_input == 'deletestocks':
            user_input = input(textwrap.dedent('''
                WARNING: This will delete all stocks and their records from the database
                Are you sure you want to delete all the stocks? ''')).strip().lower()
            if user_input[0] == 'y':
                delete_stocks()
                pass
            else:
                print()
        elif user_input == 'deleterecords':
            user_input = input(textwrap.dedent('''
                WARNING: This will delete all stocks and their records from the database
                Are you sure you want to delete all the stocks? ''')).strip().lower()
            if user_input[0] == 'y':
                delete_stock_records()
                pass
            else:
                print()
        elif user_input == 'updaterecords':
            try:
                update_stock_records()
            except:
                print('Could not update stock records.')
        elif user_input == 'printstocks':
            print('Pick exchange (left side)\n')
            for exchange in Exchange:
                print(str(exchange.value) + ': ' + exchange.name)
            print('all: Get all stocks in all available exchanges\n')
            user_input = input('Exchange: ').strip()
            if user_input == 'all':
                print_stocks()
            else:
                try:
                    print_stocks(Exchange(user_input))
                except:
                    print('Exchange not found.')
            print()
        elif user_input == 'getsuggestions':
            # output stats
            if '-v' in user_input:
                raise NotImplementedError
            # just output suggestions
            else:
                raise NotImplementedError
        elif user_input == 'cls':
            print('\n'*100)
        elif user_input == 'help':
            print(commands)
        elif user_input == '':
            pass
        else:
            print('Command not found.\n')
        user_input = get_command()


# # shows plot for price info, MACD, and RSI
# def showPlot(data, days=0):
#     data_graph1 = data[['Close', 'Boll. Upper',
#                         'Boll. Center', 'Boll. Lower', 'EMA 50', 'EMA 200']]
#     data_graph2 = data[['MACD', 'Signal']]
#     data_graph3 = data['RSI']

#     labels1 = ['Close', 'Boll. Upper', 'Boll. Center',
#                'Boll. Lower', 'EMA 50', 'EMA 200']
#     colors1 = ['k', 'r', 'orange', 'r', 'b', 'g']
#     line_widths1 = ['2', '2', '1', '2', '0.5', '0.5']
#     labels2 = ['MACD', 'Signal']
#     colors2 = ['b', 'orange']
#     line_widths2 = ['1', '1']

#     if days == 0:
#         plt.subplot(3, 1, 1)
#         ax = plt.plot(data_graph1.iloc[-31:-1],)
#     elif days > 0:
#         plt.subplot(3, 1, 1)
#         ax = plt.plot(data_graph1.iloc[(-1*days - 1):-1])
#     else:
#         print('Invalid day parameter')

#     for i, l in enumerate(ax):
#         plt.setp(l, linewidth=line_widths1[i],
#                  color=colors1[i], label=labels1[i])

#     plt.legend(loc='upper left', fontsize='x-small')
#     plt.ylabel('Closing Price')
#     plt.title('Stock Information')

#     if days == 0:
#         plt.subplot(3, 1, 2)
#         bx = plt.plot(data_graph2.iloc[-31:-1])
#     elif days > 0:
#         plt.subplot(3, 1, 2)
#         bx = plt.plot(data_graph2.iloc[(-1*days - 1):-1])
#     else:
#         print('Invalid day parameter')

#     for i, l in enumerate(bx):
#         plt.setp(l, linewidth=line_widths2[i],
#                  color=colors2[i], label=labels2[i])

#     plt.legend(loc='upper left', fontsize='x-small')
#     plt.ylabel('MACD')
#     plt.axhline(0, color='k', linewidth='0.4')

#     if days == 0:
#         plt.subplot(3, 1, 3)
#         bx = plt.plot(data_graph3.iloc[-31:-1])
#     elif days > 0:
#         plt.subplot(3, 1, 3)
#         bx = plt.plot(data_graph3.iloc[(-1*days - 1):-1])
#     else:
#         print('Invalid day parameter')

#     plt.legend(loc='upper left', fontsize='x-small')
#     plt.ylabel('RSI')
#     plt.axhline(70, color='k', linewidth='0.4')
#     plt.axhline(30, color='k', linewidth='0.4')
#     plt.show()


# # prints all data
# def outputData(data, days=0):
#     if (days == 0):
#         print()
#         print(data.tail())
#         print()
#     elif (days > 0):
#         print()
#         print(data.iloc[(-1*days - 1):-1])
#         print()
#     else:
#         print()
#         print('Invalid day parameter')
#         print()


# # prints analysis and returns values
# def outputAnalysis(data, ticker, days=0):
#     print()
#     print('---------- ' + ticker.upper() + ' Analysis ----------')

#     # Bollinger Location: top / bottom
#     boll_location = ''
#     if data['Close'].iloc[-1] > data['Boll. Center'].iloc[-1]:
#         print('Bollinger Location: Top half')
#         boll_location = 'top'
#     elif data['Close'].iloc[-1] < data['Boll. Center'].iloc[-1]:
#         print('Bollinger Location: Bottom half')
#         boll_location = 'bottom'

#     # In Bollinger Bands: Yes / Overbought / Oversold / ?
#     in_band = ''
#     if (data['High'].iloc[-1] > data['Boll. Upper'].iloc[-1] and data['Low'].iloc[-1] < data['Boll. Lower'].iloc[-1]):
#         print('In Bollinger Bands: Narrow bands or high volatility')
#         in_band = '?'
#     elif (data['High'].iloc[-1] > data['Boll. Upper'].iloc[-1]):
#         print('In Bollinger Bands: No - overbought')
#         in_band = 'overbought'
#     elif (data['Low'].iloc[-1] < data['Boll. Lower'].iloc[-1]):
#         print('In Bollinger Bands: No - oversold')
#         in_band = 'oversold'
#     else:
#         print('In Bollinger Bands: Yes')
#         in_band = 'yes'

#     # MACD Location: Greater/Less/Equals(1/-1/0) than 0
#     macd_location = ''
#     if (data['MACD'].iloc[-1] > 0):
#         print('MACD Location: Greater than 0')
#         macd_location = '1'
#     elif (data['MACD'].iloc[-1] < 0):
#         print('MACD Location: Less than 0')
#         macd_location = '-1'
#     else:
#         print('MACD Location: Equals 0')
#         macd_location = '0'

#     # Recent MACD Crossover: Buy/Sell/No
#     recent_crossover = False
#     if (data['MACD'].iloc[-1] > data['Signal'].iloc[-1]):
#         for i in range(2, 6):
#             if (data['MACD'].iloc[-1*i] <= data['Signal'].iloc[-1*i]):
#                 recent_crossover = True
#         if (recent_crossover):
#             print('Recent MACD Crossover: Yes - Buy')
#             recent_crossover = 'buy'
#         else:
#             print('Recent MACD Crossover: No')
#             recent_crossover = 'no'
#     else:
#         for i in range(2, 6):
#             if (data['MACD'].iloc[-1*i] >= data['Signal'].iloc[-1*i]):
#                 recent_crossover = True
#         if (recent_crossover):
#             print('Recent MACD Crossover: Yes - Sell')
#             recent_crossover = 'sell'
#         else:
#             print('Recent MACD Crossover: No')
#             recent_crossover = 'no'

#     # EMA support: Yes/No
#     ema_support = ''
#     if (data['EMA 50'].iloc[-1] > data['EMA 200'].iloc[-1]):
#         print('EMA Support: Yes')
#         ema_support = 'yes'
#     else:
#         print('EMA Support: No')
#         ema_support = 'no'

#     # RSI: Normal/Overbought/Oversold
#     if (data['RSI'].iloc[-1] >= 70):
#         print('RSI: Overbought')
#         rsi_support = 'overbought'
#     elif (data['RSI'].iloc[-1] <= 30):
#         print('RSI: Oversold')
#         rsi_support = 'oversold'
#     else:
#         print('RSI: Normal')
#         rsi_support = 'normal'

#     # Udacity indicators
#     if udacity_support(in_band, macd_location, recent_crossover):
#         print("Udacity: Check out this stock")
#     else:
#         print("Udacity: Nah fam")

#     analysis = [boll_location, in_band, macd_location,
#                 recent_crossover, ema_support, rsi_support]
#     score = getScore(analysis)
#     if score >= 7:
#         print('Advice: Buy')
#     elif score < 7 and score > 3:
#         print('Advice: Watch')
#     else:
#         print('Advice: Sell')


# def getScore(analysis):
#     # boll_location, in_band, macd_location, recent_crossover, ema_support, rsi_support
#     score = 0
#     if analysis[0].lower() == 'bottom':
#         score = score + 1
#     if analysis[1].lower() == 'yes':
#         score = score + 1
#     elif analysis[1].lower() == 'oversold':
#         score = score + 2
#     if analysis[2] == -1 and analysis[3].lower() == 'buy':
#         score = score + 4
#     elif analysis[3].lower() == 'buy':
#         score = score + 2
#     if analysis[4].lower() == 'yes':
#         score = score + 1
#     if analysis[5].lower() == 'oversold':
#         score = score + 3
#     elif analysis[5].lower() == 'normal':
#         score = score + 2
#     return score


# def MACD_crossover(data):
#     for i in range(5, 1, -1):
#         if data['MACD'][-1*i] <= data['Signal'][-1*i] and data['MACD'][-1*i+1] > data['Signal'][-1*i+1]:
#             return True
#     return False


# def bollinger_crossdown(data):
#     for i in range(5, 0, -1):
#         if data['Boll. Lower'][-1*i] > data['Close'][-1*i]:
#             return True
#     return False


# def udacity_support(in_band, macd_location, recent_crossover):
#     if in_band == 'oversold' and macd_location == -1 and recent_crossover == 'no':
#         return True
#     else:
#         return False


# -------------- MAIN ------------- #

if (__name__ == '__main__'):
    main()
