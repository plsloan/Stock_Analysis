import webbrowser as browser
import scrape_MACD_crossover

df = scrape_MACD_crossover.main()
symbols = df['Symbol']
symbols_under25 = df[df['Close'] <= 25]['Symbol']
for ticker in symbols_under25:
    browser.open('https://finance.yahoo.com/chart/' + ticker)