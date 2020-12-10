import webbrowser as browser
from .get_symbols import getRobinhoodSymbols


def main():
    my_stocks = getRobinhoodSymbols()
    for ticker in my_stocks:
        browser.open('https://finance.yahoo.com/chart/' + ticker)


if __name__ == '__main__':
    main()
