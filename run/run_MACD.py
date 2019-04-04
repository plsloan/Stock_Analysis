from os import system

def main():
    system('python ../scrape_MACD_crossover.py')
    system('python ../analyze_MACD.py')

if __name__ == '__main__':
    main()