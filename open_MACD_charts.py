import webbrowser as browser
import scrape_MACD_crossover

def main():
    df = scrape_MACD_crossover.main()
    symbols = df['Symbol']
    symbols_under25 = df[df['Close'] <= 25]['Symbol']
    for ticker in symbols_under25:
        browser.open('https://finance.yahoo.com/chart/' + ticker)

if __name__ == '__main__':
    main()