import webbrowser as browser
from get_symbols import getWatchlistSymbols

def main():
    date = input('Enter date (YYYY-MM-DD): ') 
    if date != '':
        watchlist_tickers = getWatchlistSymbols(date=date)
    else:
        watchlist_tickers = getWatchlistSymbols()
    for ticker in watchlist_tickers:
        browser.open('https://finance.yahoo.com/chart/' + ticker)

if __name__ == '__main__':
    main()