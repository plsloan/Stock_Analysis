import webbrowser as browser
import robin_stocks as robinhood

login = robinhood.login('phillipsloan24@gmail.com','54bR&Srkm7EU')
my_stocks = robinhood.build_holdings()
for ticker in my_stocks.keys():
    browser.open('https://finance.yahoo.com/chart/' + ticker)