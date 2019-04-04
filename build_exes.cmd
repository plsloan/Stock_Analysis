pyinstaller -F analyze_MACD.py
pyinstaller -F analyze_watchlist.py
pyinstaller -F find_ema_support.py
pyinstaller -F -w open_MACD_charts.py
pyinstaller -F -w open_robinhood_stocks.py
pyinstaller -F -w open_watchlist.py
pyinstaller -F scrape_exchange.py
pyinstaller -F -w scrape_MACD_crossover.py
pyinstaller -F scrape_symbol_list.py
pyinstaller -F stock_bot.py
pyinstaller -F update_crossover_prices.py
pyinstaller -F update_watchlist_prices.py