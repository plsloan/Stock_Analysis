import os
import scrape_symbol_list
import analyze_watchlist

def main():
    if not os.path.exists('Data/MACD_Crossover/'):
        os.makedirs('Data/MACD_Crossover/')
    if not os.path.exists('Data/NASDAQ/'):
        os.makedirs('Data/NASDAQ/')
    if not os.path.exists('Data/NYSE/'):
        os.makedirs('Data/NYSE/')
    if not os.path.exists('Data/Watchlist/'):
        os.makedirs('Data/Watchlist/')
    scrape_symbol_list.main()
    print()
    analyze_watchlist.main()

if __name__ == '__main__':
    main()