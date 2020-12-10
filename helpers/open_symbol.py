import webbrowser as browser
from .get_symbols import getWatchlistSymbols


def main():
    tickers = input('Enter ticker(s): ')

    while len(tickers) != 0 and tickers[0] != '':
        if len(tickers.split(' ')) > 1:
            tickers = tickers.split(' ')
        elif len(tickers.split(' ')) == 1:
            tickers = [tickers]
        if len(tickers) > 1:
            for ticker in tickers:
                if len(ticker) > 0:
                    browser.open('https://finance.yahoo.com/chart/' + ticker)
        elif len(tickers) == 1:
            browser.open('https://finance.yahoo.com/chart/' + tickers[0])
        tickers = input('Enter ticker(s): ')


if __name__ == '__main__':
    main()
