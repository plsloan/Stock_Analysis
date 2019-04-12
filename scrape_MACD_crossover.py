import os
import numpy
import pandas
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from update_watchlist_prices import get_trading_dates

def main(outside_use=False):
    today = datetime.now().strftime('%Y-%m-%d')
    if not (os.path.exists('Data/MACD_Crossover/' + today + '.csv' ) and today in get_trading_dates()) or outside_use:
        url = 'https://stock-screener.org/macd-crossover.aspx'
        MACD_data = get_MACD_data(url)

        csv_content = MACD_data.to_csv(index=False)
        csv_content = remove_extra_newlines(csv_content)

        today = datetime.now().strftime('%Y-%m-%d')
        if not os.path.exists('Data/MACD_Crossover/'):
            os.makedirs('Data/MACD_Crossover/')
        with open('Data/MACD_Crossover/' + today + '.csv', 'w') as file_to_write:
            file_to_write.write(csv_content)
            file_to_write.close()

        return MACD_data

# only works with stock-screener.org/macd-crossover.aspx
def get_MACD_data(url):
    req = get(url, headers={"User-Agent":"Mozilla/5.0"})
    html_soup = BeautifulSoup(req.text, 'lxml')
    table = html_soup.find('table', class_='styled')
    rows = table.find_all('tr')
    header = rows[0].find_all('th')
    data_cells = []
    data = {}
    
    labels = []
    for i in range(len(header)):
        if i != 1 and i != len(header)-1:
            labels.append(header[i].text)

    for row in rows[1:]:
        data_cells.append(row.find_all('td'))
        
    symbols        = []
    open_price     = []
    close_price    = []
    high_price     = []
    low_price      = []
    volume         = []
    percent_change = []
    for row in data_cells:
        for i in range(len(row)):
            if i == 0:
                symbols.append(row[i].text.strip())
            elif i == 2:
                open_price.append(float(row[i].text.strip()))
            elif i == 3:
                high_price.append(float(row[i].text.strip()))
            elif i == 4:
                low_price.append(float(row[i].text.strip()))
            elif i == 5:
                close_price.append(float(row[i].text.strip()))
            elif i == 6:
                volume.append(int(row[i].text.strip()))
            elif i == 7:
                percent_change.append(float(row[i].text.strip()[:-1]))
    df = pandas.DataFrame()
    df['Symbol'] = symbols
    df['Open'] = open_price
    df['High'] = high_price
    df['Low'] = low_price
    df['Close'] = close_price
    df['Volume'] = volume
    df['% Change'] = percent_change
    return df
def remove_extra_newlines(csv_string):
    if '\r\n' in csv_string:
        csv_string = csv_string.replace('\r\n', '\n')
    if '\n\n' in csv_string:
        csv_string = csv_string.replace('\n\n', '\n')
    return csv_string

if __name__ == '__main__':
    main()