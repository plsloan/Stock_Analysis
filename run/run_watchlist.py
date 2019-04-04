from os import system

def main():
    system('python ../scrape_symbol_list.py')
    system('python ../analyze_watchlist.py')

if __name__ == '__main__':
    main()