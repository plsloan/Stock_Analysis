import os
import datetime
import update_crossover_prices, update_watchlist_prices

def main():
    while datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute) < datetime.time(18, 5) and datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute) > datetime.time(7, 0):
        if datetime.datetime.now().hour in [15] and datetime.datetime.now().minute in [15]:
            print('\nUpdating MACD crossover list...')
            update_crossover_prices.main(all=True)
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        today = now.strftime('%Y-%m-%d')
        filename = now.strftime('%Y-%m-%d_%H%M') + '.csv'
        if hour in [8, 9, 10, 12, 14, 16, 18] and minute in [0]:
            filename = 'Data/Watchlist/Day0/' + today + '/' + filename
            if not os.path.exists(filename):
                print('\nUpdating ' + datetime.datetime.now().strftime('%H:%M') + '...')
                update_watchlist_prices.main(continuous=True)

if __name__ == '__main__':
    main()