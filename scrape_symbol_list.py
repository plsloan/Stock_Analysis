from datetime import datetime
import os
from requests import get 
from progressbar_mine import progress_bar_mine

def main():
    tickers = input('Enter list of symbols (separated by space): ').split(' ')
    progress_bar = progress_bar_mine(len(tickers))
    progress_bar.start()
    for i in range(len(tickers)):
        scrape_symbol(tickers[i])
        progress_bar.update(i)
    progress_bar.finish()

def scrape_symbol(ticker):
    date = datetime.now().strftime('%Y-%m-%d')
    path = 'Data/Watchlist/' + date + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    failed_pull = []
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
if __name__ == '__main__':
    main()