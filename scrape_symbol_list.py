import pandas
import shutil

from datetime import datetime
from requests import get 
from progressbar_mine import progress_bar_mine

import os
from os import listdir
from os.path import isfile, join

from update_crossover_prices import get_ticker_price

def main():
    # get 
    tickers = input('Enter list of symbols (separated by space): ').split(' ')
    progress_bar = progress_bar_mine(len(tickers))
    progress_bar.start()
    for i in range(len(tickers)):
        scrape_symbol(tickers[i])
        progress_bar.update(i)
    progress_bar.finish()
    compile_file(tickers)

def scrape_symbol(ticker):
    path = 'Data/Watchlist/Temp/'
    if not os.path.exists(path):
        os.makedirs(path)
    failed_pull = []
    date = datetime.now().strftime('%Y-%m-%d')
    url = 'http://quotes.wsj.com/' + ticker + '/historical-prices/download?MOD_VIEW=page&num_rows=6299.041666666667&range_days=6299.041666666667&startDate=01/01/2010&endDate=' + date
    content = get(url).text
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

def compile_file(tickers):
    date = datetime.now().strftime('%Y-%m-%d')
    data = []
    updated_prices = []
    path = 'Data/Watchlist/Temp/'
    for csv_file in [f for f in listdir(path) if isfile(join(path, f))]:
        filename = path + csv_file
        data.append(pandas.read_csv(filename, delimiter=', ', engine='python'))
    for ticker in tickers:
        try:
            updated_prices.append(float(get_ticker_price(ticker)))
        except:
            updated_prices.append(-1.0)
    shutil.rmtree(path, ignore_errors=True)
    df = pandas.DataFrame(columns=data[0].keys())
    for d in data:
        df = df.append(d.iloc[0])
    df['Symbol'] = tickers
    # df[date] = updated_prices
    df.to_csv('Data/Watchlist/' + date + '.csv', index=False)

if __name__ == '__main__':
    main()