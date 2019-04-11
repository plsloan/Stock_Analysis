import os
import numpy
import pandas
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    if not os.path.exists('Data/MACD_Crossover/' + today + '.csv' ):
        url = 'https://stock-screener.org/macd-crossover.aspx'
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

        csv_content = df.to_csv(index=False)
        if '\r\n' in csv_content:
            csv_content = csv_content.replace('\r\n', '\n')
        if '\n\n' in csv_content:
            csv_content = csv_content.replace('\n\n', '\n')
        year = str(datetime.now().strftime('%Y'))
        month = str(datetime.now().strftime('%m'))
        day = str(datetime.now().strftime('%d'))
        hour = str(datetime.now().strftime('%H'))
        minute = str(datetime.now().strftime('%M'))

        if not os.path.exists('Data/MACD_Crossover/'):
            os.makedirs('Data/MACD_Crossover/')
        with open('Data/MACD_Crossover/' + year + '-' + month + '-' + day + '.csv', 'w') as filetowrite:#'___' + hour + '-' + minute + '.csv', 'w') as filetowrite:
            filetowrite.write(csv_content)
            filetowrite.close()

        return df


if __name__ == '__main__':
    main()