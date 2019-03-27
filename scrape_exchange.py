import os
from requests import get 
from datetime import datetime
from get_symbols import get_nasdaq_tickers, get_nyse_tickers


def main():
    response = input("Exchange (Nasdaq/NYSE/both): ")

    if response.lower()[:2] == 'na':
        try:
            tickers = get_nasdaq_tickers()
        except:
            print("Couldn't find file with tickers...")
            return -1
        if not os.path.exists('Data/NASDAQ/'):
            os.makedirs('Data/NASDAQ/')
        scrape_historical_data(tickers, response)
    elif response.lower()[:2] == 'ny':
        try:
            tickers = get_nyse_tickers()
        except:
            print("Couldn't find file with tickers...")
            return -1
        if not os.path.exists('Data/NYSE/'):
            os.makedirs('Data/NYSE/')
        scrape_historical_data(tickers, response)
    elif response.lower()[0] == 'b':
        pass
    else:
        print('Something was misspelled...')

def scrape_historical_data(tickers, res):
    now = datetime.now()
    today = str(now.month) + '/' + str(now.day) + '/' + str(now.year)
    for ticker in tickers:
        url = 'http://quotes.wsj.com/' + ticker + '/historical-prices/download?MOD_VIEW=page&num_rows=6299.041666666667&range_days=6299.041666666667&startDate=01/01/2010&endDate=' + today
        content = get(url).text
        if res[:2] == 'na':
            path = 'Data/NASDAQ/'
        else:
            path = 'Data/NYSE/'
        f = open(path + ticker + '.csv','w')
        f.write(content)
        f.close()

if __name__ == "__main__":
    main()