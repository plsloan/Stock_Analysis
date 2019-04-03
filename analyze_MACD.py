import pandas
import glob
from datetime import datetime
import update_crossover_prices

now = datetime.now()
path = 'Data/MACD_Crossover/'
newest_column = now.strftime('%Y-%m-%d')

def main():
    csv_files = glob.glob(path + '*.csv')
    gainer_list = []
    loser_list = []
    for csv in csv_files:
        df = pandas.read_csv(csv)
        if newest_column not in df.keys():
            update_crossover_prices.main()
            df = pandas.read_csv(path + csv)
        gainers = df[df['Close'] < df[newest_column]]
        losers = df[df['Close'] >= df[newest_column]]
        gainer_list.append(gainers)
        loser_list.append(losers)
        

        

if __name__=='__main__':
    main()