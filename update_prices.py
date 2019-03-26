import pandas
from requests import get
from bs4 import BeautifulSoup

def main():
    filename = input("Enter date (YYYY-MM-DD): ")
    filename = 'Data/MACD_Crossover/' + filename + '.csv'
    df = pandas.read_csv(filename)
    tickers = df['Symbol']

    updated_prices = []
    for ticker in tickers:
        try:
            updated_prices.append(get_ticker_price(ticker))
        except:
            updated_prices.append(-1)

    df['Updated_Price'] = updated_prices
    df.to_csv(filename)

def get_ticker_price(ticker):
    url = 'https://finance.yahoo.com/quote/' + ticker
    html = BeautifulSoup(get(url).content, features="lxml")
    header = html.find('div', id="quote-header-info")
    divs = header.find_all('div')
    return(divs[7].find('div').find('span').text)

if __name__ == "__main__":
    main()