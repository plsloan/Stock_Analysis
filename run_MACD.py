import os
import scrape_MACD_crossover
import analyze_MACD

def main():
    if not os.path.exists('Data/MACD_Crossover/'):
        os.makedirs('Data/MACD_Crossover/')
    if not os.path.exists('Data/NASDAQ/'):
        os.makedirs('Data/NASDAQ/')
    if not os.path.exists('Data/NYSE/'):
        os.makedirs('Data/NYSE/')
    if not os.path.exists('Data/Watchlist/'):
        os.makedirs('Data/Watchlist/')
    scrape_MACD_crossover.main()
    print()
    analyze_MACD.main()

if __name__ == '__main__':
    main()