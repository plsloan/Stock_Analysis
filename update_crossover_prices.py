import glob
import pandas
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from progressbar_mine import progress_bar_mine

column_name = datetime.now().strftime('%Y-%m-%d')

def main():
    response = input('all? ')
    path = 'Data/MACD_Crossover/'
    if (response == '' or response.lower()[0] == 'y'):
        csv_files = glob.glob(path + '*.csv')
        progress_bar = progress_bar_mine(max_val=len(csv_files), transfer_speed=False)
        progress_bar.start()
        for csv_file in csv_files:
            df = pandas.read_csv(csv_file)
            tickers = df['Symbol']
            updated_prices = []
            for ticker in tickers:
                try:
                    updated_prices.append(float(get_ticker_price(ticker)))
                except:
                    updated_prices.append(-1.0)
            df[column_name] = updated_prices
            gain_values = df[column_name] - df['Close']
            for i in range(len(gain_values)):
                gain_values[i] = round(gain_values[i], 2)
            df['Gain'] = gain_values
            gainers = df[df['Gain'] > 0]
            # keep Gain column last
            if df.keys()[-1] != 'Gain':
                cols = list(df.keys())
                cols = cols[:-2] + [cols[-1]] + [cols[-2]]
                df = df[cols]
            # print('\nGainers -', csv_file.split('\\')[1][:-4].replace('-', '/'))
            # print(gainers)
            # print("\n\nAccuracy:", str("{0:.2f}".format(float(len(gainers)/len(df)*100))) + '%', '(' + str(len(gainers)) + '/' + str(len(df)) + ')')
            # print('\n')
            df.to_csv(csv_file, index=False)
            progress_bar.update(csv_files.index(csv_file))
        progress_bar.finish()

    elif response.lower()[0] == 'n':
        filename = input("Enter date (YYYY-MM-DD): ")
        filename = path + filename + '.csv'
        df = pandas.read_csv(filename)
        tickers = df['Symbol']
        updated_prices = []
        for ticker in tickers:
            try:
                updated_prices.append(float(get_ticker_price(ticker)))
            except:
                updated_prices.append(-1.0)
        df[column_name] = updated_prices
        gain_values = df[column_name] - df['Close']
        for i in range(len(gain_values)):
            gain_values[i] = round(gain_values[i], 2)
        df['Gain'] = gain_values
        gainers = df[df['Gain'] > 0]
        # keep Gain column last
        if df.keys()[-1] != 'Gain':
            cols = list(df.keys())
            cols = cols[:-2] + [cols[-1]] + [cols[-2]]
            df = df[cols]
        print('\nGainers -', filename.split('/')[2][:-4].replace('-', '/'))
        print(gainers)
        print("\n\nAccuracy:", str("{0:.2f}".format(float(len(gainers)/len(df)*100))) + '%', '(' + str(len(gainers)) + '/' + str(len(df)) + ')')
        df.to_csv(filename, index=False)
        print('\n')
        
def get_ticker_price(ticker):
    url = 'https://finance.yahoo.com/quote/' + ticker
    html = BeautifulSoup(get(url).content, features="lxml")
    header = html.find('div', id="quote-header-info")
    divs = header.find_all('div')
    return(divs[7].find('div').find('span').text)

if __name__ == "__main__":
    main()