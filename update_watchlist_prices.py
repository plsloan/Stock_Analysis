import os
import glob
import pandas
from requests import get
from bs4 import BeautifulSoup

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from progressbar_mine import progress_bar_mine
from pandas_datareader import data as pdr
import fix_yahoo_finance

from update_crossover_prices import get_ticker_price
import analyze_watchlist

now = datetime.now()
path = 'Data/Watchlist/'
column_name = now.strftime('%Y-%m-%d')
hour_minute = now.strftime('%H%M')

def main():
    response = input('all? ')
    path = 'Data/Watchlist/'
    if (response == '' or response.lower()[0] == 'y'):
        csv_files = glob.glob(path + '*.csv')
        progress_bar = progress_bar_mine(max_val=len(csv_files), transfer_speed=False)
        progress_bar.start()
        for csv_file in csv_files:
            progress_bar.update(csv_files.index(csv_file))
            df = pandas.read_csv(csv_file)
            tickers = df['Symbol']
            updated_prices = []
            for ticker in tickers:
                try:
                    updated_prices.append(float(get_ticker_price(ticker)))
                except:
                    updated_prices.append(-1.0)
            df[column_name] = updated_prices
            gain_values = df[column_name] - df['Close']
            for i in range(len(gain_values)):
                gain_values[i] = round(gain_values[i], 2)
            df['Gain'] = gain_values
            gainers = df[df['Gain'] > 0]
            # keep Gain column last
            if df.keys()[-1] != 'Gain':
                cols = list(df.keys())
                cols = cols[:-2] + [cols[-1]] + [cols[-2]]
                df = df[cols]
            # print('\nGainers -', csv_file.split('\\')[1][:-4].replace('-', '/'))
            # print(gainers)
            # print("\n\nAccuracy:", str("{0:.2f}".format(float(len(gainers)/len(df)*100))) + '%', '(' + str(len(gainers)) + '/' + str(len(df)) + ')')
            # print('\n')
            df.to_csv(csv_file[:-4] + '.csv', index=False)
            organize_data(df, csv_file[:-4] + '_' + hour_minute + '.csv')
        progress_bar.finish()
    elif (response.lower()[0] == 'n'):
        filename = input("Enter date (YYYY-MM-DD): ")
        filename = path + filename + '.csv'
        df = pandas.read_csv(filename)
        tickers = df['Symbol']
        updated_prices = []
        for ticker in tickers:
            try:
                updated_prices.append(float(get_ticker_price(ticker)))
            except:
                updated_prices.append(-1.0)
        df[column_name] = updated_prices
        gain_values = df[column_name] - df['Close']
        for i in range(len(gain_values)):
            gain_values[i] = round(gain_values[i], 2)
        df['Gain'] = gain_values
        gainers = df[df['Gain'] > 0]
        # keep Gain column last
        if df.keys()[-1] != 'Gain':
            cols = list(df.keys())
            cols = cols[:-2] + [cols[-1]] + [cols[-2]]
            df = df[cols]
        print('\nGainers -', filename.split('/')[2][:-4].replace('-', '/'))
        print(gainers)
        print("\n\nAccuracy:", str("{0:.2f}".format(float(len(gainers)/len(df)*100))) + '%', '(' + str(len(gainers)) + '/' + str(len(df)) + ')')
        df.to_csv(filename[:-4] + '.csv', index=False)
        organize_data(df, filename[:-4] + '_' + hour_minute + '.csv')
    analyze_watchlist.main()

def get_trading_dates():
    end_date = datetime.now()
    start_date = end_date - relativedelta(months=1)
    data = pdr.get_data_yahoo('^GSPC', start=start_date, end=end_date)
    return data.index.strftime('%Y-%m-%d').tolist()
def organize_data(data, filename):
    path = 'Data/Watchlist/'
    filename = filename.replace('\\', '/')
    date_split = filename.split('/')[-1].split('_')[0].split('-')
    then = datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
    now = datetime.today()
    trading_dates = get_trading_dates()
    increment_count = 0
    for i in range(1, len(trading_dates)+1):
        if trading_dates[i*-1] == then.strftime('%Y-%m-%d'):
            break
        increment_count = increment_count + 1
    should_organize = False
    if increment_count <= 7:
        if increment_count in [0, 1, 3, 5]:
            path = path + 'Day' + str(increment_count) + '/'
            should_organize = True
        elif increment_count == 7:
            path = path + 'Week1/'
            should_organize = True
    elif increment_count > 7:
        delta = now - then
        if delta.days % 7 == 0 and delta/7 <= 4:
            path = path + 'Week' + str(int(delta/7)) + '/'
            should_organize = True
        elif then.month - now.month == 1 and then.day - now.day == 0:
            path = path + 'Month/'
            should_organize = True
    if should_organize:
        filename = path + filename.split('/')[-1].split('_')[0] + '/' + filename.split('/')[-1]
        if not os.path.exists('/'.join(filename.split('/')[:-1])):
            os.makedirs('/'.join(filename.split('/')[:-1]))
        data.to_csv(filename, index=False)

if __name__ == "__main__":
    main()