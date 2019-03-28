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
        try:
            tickers = get_nasdaq_tickers()
            if not os.path.exists('Data/NASDAQ/'):
                os.makedirs('Data/NASDAQ/')
            scrape_historical_data(tickers, 'nasdaq')

            tickers = get_nyse_tickers()
            if not os.path.exists('Data/NYSE/'):
                os.makedirs('Data/NYSE/')
            scrape_historical_data(tickers, 'nyse')
        except:
            print("Couldn't find file with tickers...")
            return -1
        
    else:
        print('Something was misspelled...')


def scrape_historical_data(tickers, exchange):
    now = datetime.now()
    today = str(now.month) + '/' + str(now.day) + '/' + str(now.year)
    failed_pull = []
    for ticker in tickers:
        url = 'http://quotes.wsj.com/' + ticker + '/historical-prices/download?MOD_VIEW=page&num_rows=6299.041666666667&range_days=6299.041666666667&startDate=01/01/2010&endDate=' + today
        content = get(url).text
        if exchange[:2] == 'na':
            path = 'Data/NASDAQ/'
        elif exchange[:2] == 'ny':
            path = 'Data/NYSE/'
        try:
            f = open(path + ticker + '.csv','w')
            f.write(content)
            f.close()
        except:
            failed_pull.append(ticker)
    # write failed pulls
    if len(failed_pull) > 0:
        content = 'Symbol\n'
        f = open(path + '_failed_pulls.csv','w')
        for ticker in failed_pull:
            content = content + ticker + '\n'
        f.write(content)
        f.close()


if __name__ == "__main__":
    main()