import glob
import pandas
import warnings
from requests import get
from datetime import datetime
from bs4 import BeautifulSoup
from _lib.progressbar_mine import progress_bar_mine
from alpha_vantage.timeseries import TimeSeries
import analyze_MACD

path = 'Data/MACD_Crossover/'
column_name = datetime.now().strftime('%Y-%m-%d')
warnings.simplefilter(action='ignore', category=FutureWarning)
time_series = TimeSeries(key='5TBOUP0SFMZDQSWR', output_format='pandas')

# has two large if statements, because of loop in the first
def main(all=False):
    if all:
        response = 'y'
    else:
        response = input('all? ')
    if (response == '' or response.lower()[0] == 'y'):
        csv_files = glob.glob(path + '*.csv')
        progress_bar = progress_bar_mine(max_val=len(csv_files), transfer_speed=False)
        progress_bar.start()
        for csv_file in csv_files:
            progress_bar.update(csv_files.index(csv_file))
            df = pandas.read_csv(csv_file)
            df[column_name] = get_updated_prices(df)
            if len(df[df[column_name] == 'NaN']) > 0:
                df.drop(df[df[column_name] == 'NaN'].index, inplace=True)
            gain_values = df[column_name] - df['Close']
            for i in range(len(gain_values)):
                gain_values.iloc[i] = round(gain_values.iloc[i], 2)
            df['Gain'] = gain_values
            gainers = df[df['Gain'] > 0]
            # shift gain column to last column
            if df.keys()[-1] != 'Gain':
                cols = list(df.keys())
                cols = cols[:-2] + [cols[-1]] + [cols[-2]]
                df = df[cols]
            df.to_csv(csv_file, index=False)
        progress_bar.finish()
    elif response.lower()[0] == 'n':
        filename = input("Enter date (YYYY-MM-DD): ")
        filename = path + filename + '.csv'
        df = pandas.read_csv(filename)
        df[column_name] = get_updated_prices(df)
        if len(df[df[column_name] == 'NaN']) > 0:
            df.drop(df[df[column_name] == 'NaN'].index, inplace=True)
        gain_values = df[column_name] - df['Close']
        for i in range(len(gain_values)):
            gain_values.iloc[i] = round(gain_values.iloc[i], 2)
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
    analyze_MACD.main()
    
def get_ticker_price(ticker):
    try: 
        data, meta_data = time_series.get_intraday(symbol=ticker,interval='1min', outputsize='compact')
        if data.iloc[-1][3] != -1:
            return data.iloc[-1][3]
        else:
            url = 'https://finance.yahoo.com/quote/' + ticker
            html = BeautifulSoup(get(url).content, features="lxml")
            header = html.find('div', id="quote-header-info")
            divs = header.find_all('div')
            return(divs[7].find('div').find('span').text)
    except:
        url = 'https://finance.yahoo.com/quote/' + ticker
        html = BeautifulSoup(get(url).content, features="lxml")
        header = html.find('div', id="quote-header-info")
        divs = header.find_all('div')
        return(divs[7].find('div').find('span').text)
def get_updated_prices(df):
    tickers = df['Symbol']
    updated_prices = []
    for ticker in tickers:
        try:
            updated_prices.append(float(get_ticker_price(ticker)))
        except:
            updated_prices.append('NaN')
    return updated_prices
if __name__ == "__main__":
    main()