import glob
import pandas
from os import listdir
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from os.path import isfile, join
from progressbar_mine import progress_bar_mine
from update_crossover_prices import get_gainers, get_ticker_price

now = datetime.now()
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
            df = pandas.read_csv(csv_file)
            tickers = df['Symbol']
            updated_prices = []
            for ticker in tickers:
                try:
                    updated_prices.append(float(get_ticker_price(ticker)))
                except:
                    updated_prices.append(-1.0)
            df[column_name] = updated_prices
            gainers = get_gainers(df)
            # print('\nGainers -', csv_file.split('\\')[1][:-4].replace('-', '/'))
            # print(gainers)
            # print("\n\nAccuracy:", str("{0:.2f}".format(float(len(gainers)/len(df)*100))) + '%', '(' + str(len(gainers)) + '/' + str(len(df)) + ')')
            # print('\n')
            df.to_csv(csv_file[:-4] + '.csv', index=False)
            df.to_csv(csv_file[:-4] + '_' + hour_minute + '.csv', index=False)
            progress_bar.update(csv_files.index(csv_file))
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
        gainers = get_gainers(df)
        print('\nGainers -', filename.split('/')[2][:-4].replace('-', '/'))
        print(gainers)
        print("\n\nAccuracy:", str("{0:.2f}".format(float(len(gainers)/len(df)*100))) + '%', '(' + str(len(gainers)) + '/' + str(len(df)) + ')')
        df.to_csv(filename[:-4] + '.csv', index=False)
        df.to_csv(filename[:-4] + '_' + hour_minute + '.csv', index=False)

if __name__ == "__main__":
    main()