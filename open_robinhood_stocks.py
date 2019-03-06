import webbrowser as browser
from get_symbols import getRobinhoodSymbols

my_stocks = getRobinhoodSymbols()
for ticker in my_stocks:
    browser.open('https://finance.yahoo.com/chart/' + ticker)