import sys
sys.path.append('..')
import scrape_symbol_list
import analyze_watchlist
from os import chdir

def main():
    chdir('..')
    scrape_symbol_list.main()
    print()
    analyze_watchlist.main()

if __name__ == '__main__':
    main()