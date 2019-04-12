import os
import glob
import pandas
from datetime import datetime
import update_watchlist_prices
from _lib.helpers import get_directories, find_file

now = datetime.now()
newest_column = now.strftime('%Y-%m-%d')

def main():
    path = 'Data/Watchlist/'
    csv_files = glob.glob(path + '*.csv')
    analyze(path, csv_files, main_folder=True)
    directories = get_directories(path)
    analyze_subdirectories(path, directories)
    

def addToContent(content, label, df):
    content = content + label + str(len(df)) + '\n' 
    return content
def analyze(path, glob, main_folder=False):
    content = ''
    if main_folder:
        for csv in glob:
            if '_' not in csv:
                df = pandas.read_csv(csv)
                # update_input = input('Update first? ')
                # if newest_column not in df.keys():
                #     if update_input.lower()[0] == 'y':
                #         update_watchlist_prices.main()
                #         df = pandas.read_csv(csv)
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
    else:
        for csv in glob:
            df = pandas.read_csv(csv)
            # update_input = input('Update first? ')
            # if newest_column not in df.keys():
            #     if update_input.lower()[0] == 'y':
            #         update_watchlist_prices.main()
            #         df = pandas.read_csv(csv)
            under25 = df[df['Close'] <= 25]
            above25 = df[df['Close'] > 25]
            gainers = df[df['Gain'] > 0]
            losers = df[df['Gain'] <= 0]
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
                content = content + ' * Total Gain: $' + str("{0:.2f}".format(df['Gain'].sum())) + '\n'
                content = content + ' * Accuracy: ' + str("{0:.2f}".format(float(len(gainers)/len(df))*100)) + '%\n'
                content = content + '\n'
                if len(under25) > 0 and len(df) != len(under25):
                    content = addToContent(content, ' * Gainers < 25: ', gainers_under25)
                    content = addToContent(content, ' * Losers < 25: ', losers_under25)
                    content = content + ' * Total Gain: $' + str("{0:.2f}".format((under25['Gain'].sum()))) + '\n'
                    content = content + ' * Accuracy: ' + str("{0:.2f}".format(float(len(gainers_under25)/len(under25))*100)) + '%\n'
                    content = content + '\n'
                if len(above25) > 0 and len(df) != len(above25):
                    content = addToContent(content, ' * Gainers > 25: ', gainers_above25)
                    content = addToContent(content, ' * Losers > 25: ', losers_above25)
                    content = content + ' * Total Gain: $' + str("{0:.2f}".format(above25['Gain'].sum())) + '\n'
                    content = content + ' * Accuracy: ' + str("{0:.2f}".format(float(len(gainers_above25)/len(above25))*100)) + '%\n'
            content = content + '\n\n\n'
        f = open(path + 'analyze.txt', "w")
        f.write(content)
        f.close()
def analyze_subdirectories(path, directories):
    for directory in directories:
        path = path + directory + '/'
        subdir = get_directories(path)
        recent_files = []
        for sub in subdir:
            sub_path = path + sub + '/'
            recent_files.append(glob.glob(sub_path + '*.csv')[-1])
            sub_path = 'Data/Watchlist/' + directory + '/'
        analyze(path, recent_files)
        path = 'Data/Watchlist/'


if __name__=='__main__':
    main()