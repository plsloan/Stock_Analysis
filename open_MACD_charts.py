import pandas
from datetime import datetime
import webbrowser as browser
from my_enums import StockColumn, StockRecordsColumn


def main(already_scraped=False):
    if not already_scraped:
        df = scrape_MACD_crossover.main(outside_use=True)
    else:
        today = datetime.now().strftime('%Y-%m-%d')
        df = pandas.read_csv('Data/MACD_Crossover/' + today + '.csv')
    symbols = df[StockColumn.Symbol.name]
    symbols_under25 = df[df[StockRecordsColumn.Close.name]
                         <= 25][StockColumn.Symbol.name]
    for ticker in symbols_under25:
        browser.open('https://finance.yahoo.com/chart/' + ticker)


if __name__ == '__main__':
    main()
