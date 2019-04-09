import pandas
import glob
from datetime import datetime
import update_watchlist_prices

now = datetime.now()
path = 'Data/Watchlist/'
newest_column = now.strftime('%Y-%m-%d')

def main():
    csv_files = glob.glob(path + '*.csv')
    content = ''
    for csv in csv_files:
        if '_' not in csv:
            df = pandas.read_csv(csv)
            if newest_column not in df.keys():
                update_watchlist_prices.main()
                df = pandas.read_csv(csv)
            under25 = df[df['Close'] <= 25]
            above25 = df[df['Close'] > 25]
            gainers = df[df['Close'] < df[newest_column]]
            losers = df[df['Close'] >= df[newest_column]]
            gainers_under25 = gainers[gainers['Close'] <= 25.0]
            gainers_above25 = gainers[gainers['Close'] > 25.0]
            losers_under25 = losers[losers['Close'] <= 25.0]
            losers_above25 = losers[losers['Close'] > 25.0]
            content = content + csv.split('\\')[1][:-4] + '\n\n'
            if len(gainers) > 0:
                content = addToContent(content, ' * Gainers: ', gainers)
            if len(losers) > 0:
                content = addToContent(content, ' * Losers: ', losers)
            if len(df) > 0:
                content = content + ' * Total Gain: $' + str("{0:.2f}".format((df[newest_column] - df['Close']).sum())) + '\n'
                content = content + ' * Accuracy: ' + str("{0:.2f}".format(float(len(gainers)/len(df))*100)) + '%\n'
                content = content + '\n'
                if len(under25) > 0 and len(df) != len(under25):
                    content = addToContent(content, ' * Gainers < 25: ', gainers_under25)
                    content = addToContent(content, ' * Losers < 25: ', losers_under25)
                    content = content + ' * Total Gain: $' + str("{0:.2f}".format((under25[newest_column] - under25['Close']).sum())) + '\n'
                    content = content + ' * Accuracy: ' + str("{0:.2f}".format(float(len(gainers_under25)/len(under25))*100)) + '%\n'
                    content = content + '\n'
                if len(above25) > 0 and len(df) != len(above25):
                    content = addToContent(content, ' * Gainers > 25: ', gainers_above25)
                    content = addToContent(content, ' * Losers > 25: ', losers_above25)
                    content = content + ' * Total Gain: $' + str("{0:.2f}".format((above25[newest_column] - above25['Close']).sum())) + '\n'
                    content = content + ' * Accuracy: ' + str("{0:.2f}".format(float(len(gainers_above25)/len(above25))*100)) + '%\n'
            content = content + '\n\n\n'
    f = open(path + 'analyze.txt', "w")
    f.write(content)
    f.close()


def addToContent(content, label, df):
    content = content + label + str(len(df)) + '\n' 
    return content

if __name__=='__main__':
    main()