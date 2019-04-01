import pandas
from os import listdir
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from os.path import isfile, join
from update_crossover_prices import get_gainers, get_ticker_price

column_name = datetime.now().strftime('%Y-%m-%d')

def main():
    response = input('all? ')
    path = 'Data/Watchlist/'
    if (response == '' or response.lower()[0] != 'n'):
        for csv_file in [f for f in listdir(path) if isfile(join(path, f))]:
            filename = path + csv_file
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
            print(gainers)
            print("Accuracy:", len(gainers)/len(df))
            df.to_csv(filename, index=False)
            print('\n\n')
    else:
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
        print('Gainers')
        print(gainers)
        print("\n\nAccuracy:", len(gainers)/len(df), '(' + str(len(gainers)) + '/' + str(len(df)) + ')')
        df.to_csv(filename, index=False)

if __name__ == "__main__":
    main()