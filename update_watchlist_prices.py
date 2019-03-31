import pandas
from os import listdir
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from os.path import isfile, join

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
        print(gainers)
        print("Accuracy:", len(gainers)/len(df))
        df.to_csv(filename, index=False)
        
def get_ticker_price(ticker):
    url = 'https://finance.yahoo.com/quote/' + ticker
    html = BeautifulSoup(get(url).content, features="lxml")
    header = html.find('div', id="quote-header-info")
    divs = header.find_all('div')
    return(divs[7].find('div').find('span').text)

def get_gainers(df):
    column = df.keys()[-1]
    return df[df[column] > df['Close']]

if __name__ == "__main__":
    main()