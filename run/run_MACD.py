import sys
sys.path.append('..')
import scrape_MACD_crossover
import analyze_MACD
from os import chdir

def main():
    chdir('..')
    scrape_MACD_crossover.main()
    print()
    analyze_MACD.main()

if __name__ == '__main__':
    main()