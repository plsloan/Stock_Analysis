pyinstaller.exe -F ./analyze_MACD.py
pyinstaller.exe -F ./analyze_watchlist.py
pyinstaller.exe -F ./find_ema_support.py
pyinstaller.exe -F -w open_MACD_charts.py
pyinstaller.exe -F -w open_robinhood_stocks.py
pyinstaller.exe -F -w open_watchlist.py
pyinstaller.exe -F ./scrape_exchange.py
pyinstaller.exe -F -w scrape_MACD_crossover.py
pyinstaller.exe -F ./scrape_symbol_list.py
pyinstaller.exe -F ./stock_bot.py
pyinstaller.exe -F ./update_crossover_prices.py
pyinstaller.exe -F ./update_watchlist_prices.py
pyinstaller.exe -F -w run/run_MACD.py
pyinstaller.exe -F -w run/run_watchlist.py