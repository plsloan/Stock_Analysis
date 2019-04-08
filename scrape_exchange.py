import os
import pandas
from requests import get 
from datetime import datetime
from iexfinance import get_stats_daily
from progressbar_mine import progress_bar_mine
from alpha_vantage.timeseries import TimeSeries
from get_symbols import get_nasdaq_tickers, get_nyse_tickers

time_series = TimeSeries(key='5TBOUP0SFMZDQSWR', output_format='pandas')

def main():
    response = input("Exchange (Nasdaq/NYSE/both): ")
    print_time()

    if response.lower()[:2] == 'na':
        try:
            tickers = get_nasdaq_tickers()
            if not os.path.exists('Data/NASDAQ/'):
                os.makedirs('Data/NASDAQ/')
        except:
            print("Couldn't find file with tickers...")
            return -1
        try:
            scrape_historical_data(tickers, response)
        except: 
            print('Error occurred while scraping...')
            return -1
        print_time()
    elif response.lower()[:2] == 'ny':
        try:
            tickers = get_nyse_tickers()
            if not os.path.exists('Data/NYSE/'):
                os.makedirs('Data/NYSE/')
        except:
            print("Couldn't find file with tickers...")
            return -1
        try:
            scrape_historical_data(tickers, response)
        except: 
            print('Error occurred while scraping...')
            return -1
        print_time()

    elif response.lower()[0] == 'b':
        try:
            tickers = get_nasdaq_tickers()
            if not os.path.exists('Data/NASDAQ/'):
                os.makedirs('Data/NASDAQ/')
            print('Scraping Nasdaq...')
            try:
                scrape_historical_data(tickers, 'nasdaq')
            except: 
                print('Error occurred while scraping...')
                return -1

            tickers = get_nyse_tickers()
            if not os.path.exists('Data/NYSE/'):
                os.makedirs('Data/NYSE/')
            print('Scraping NYSE...')
            try:
                scrape_historical_data(tickers, 'nyse')
            except: 
                print('Error occurred while scraping...')
                return -1
            print_time()
        except:
            print("Couldn't find file with tickers...")
            return -1
        
    else:
        print('Something was misspelled...')


def scrape_historical_data(tickers, exchange):
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    failed_pull = []
    start_date= pandas.to_datetime('2016-01-01')
    end_date= today
    progress_bar = progress_bar_mine(max_val=len(tickers))
    progress_bar.start()
    for i in range(len(tickers)):
        try:
            progress_bar.update(i)
            data = time_series.get_daily(symbol=tickers[i], outputsize='compact')[0]
            data = pandas.DataFrame(data)
            if exchange[:2] == 'na':
                path = 'Data/NASDAQ/'
            elif exchange[:2] == 'ny':
                path = 'Data/NYSE/'
            data.reset_index(level=0, inplace=True)
            data.rename(index=str, columns={'date':'Date', '1. open':'Open', '2. high':'High', '3. low':'Low', '4. close':'Close', '5. volume':'Volume'}, inplace=True)
            data.to_csv(path + tickers[i] + '.csv')
        except:
            url = 'http://quotes.wsj.com/' + tickers[i] + '/historical-prices/download?MOD_VIEW=page&num_rows=6299.041666666667&range_days=6299.041666666667&startDate=01/01/2010&endDate=' + today
            content = get(url).text
            if exchange[:2] == 'na':
                path = 'Data/NASDAQ/'
            elif exchange[:2] == 'ny':
                path = 'Data/NYSE/'
            try:
                f = open(path + tickers[i] + '.csv','w')
                f.write(content)
                f.close()
            except:
                failed_pull.append(tickers[i])
        if len(failed_pull) > 0:
            content = 'Symbol\n'
            f = open(path + '_failed_pulls.csv','w')
            for ticker in failed_pull:
                content = content + ticker + '\n'
            f.write(content)
            f.close()
    progress_bar.finish()

    #     url = 'http://quotes.wsj.com/' + tickers[i] + '/historical-prices/download?MOD_VIEW=page&num_rows=6299.041666666667&range_days=6299.041666666667&startDate=01/01/2010&endDate=' + today
    #     content = get(url).text
    #     if exchange[:2] == 'na':
    #         path = 'Data/NASDAQ/'
    #     elif exchange[:2] == 'ny':
    #         path = 'Data/NYSE/'
    #     try:
    #         f = open(path + tickers[i] + '.csv','w')
    #         f.write(content)
    #         f.close()
    #     except:
    #         failed_pull.append(tickers[i])
    #     progress_bar.update(i)
    # progress_bar.finish()
    # write failed pulls
    # if len(failed_pull) > 0:
    #     content = 'Symbol\n'
    #     f = open(path + '_failed_pulls.csv','w')
    #     for ticker in failed_pull:
    #         content = content + ticker + '\n'
    #     f.write(content)
    #     f.close()
def print_time():
    print(datetime.now().strftime('%H:%M'))

if __name__ == "__main__":
    main()