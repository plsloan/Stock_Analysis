from progressbar import ProgressBar, Bar, Percentage, ETA, FileTransferSpeed
import numpy as np


def strip_string(s):
    return s.replace(' ', '').replace('\t', '')


def get_command():
    return strip_string(input('StockBot: ').lower())


def convert_dataframe_to_document(df):
    df = calculate_adjusted_prices(df)
    document = []
    for i in range(len(df)):
        record = {}
        record['Date'] = str(df.iloc[i].name)[:-9]
        for k in df.keys():
            record[k] = df.iloc[i][k]
        document.append(record)
    return document


def calculate_adjusted_prices(df):
    """ Vectorized approach for calculating the adjusted prices for the
    specified column in the provided DataFrame. This creates a new column
    called 'adj_<column name>' with the adjusted prices. This function requires
    that the DataFrame have columns with dividend and split_ratio values.


    :param df: DataFrame with raw prices along with dividend and split_ratio
        values
    :return: DataFrame with the addition of the adjusted price column
    """
    column = 'Close'
    adj_column = 'Adjusted Close'
    dividends_column = 'Dividends'
    splits_column = 'Stock Splits'

    # Reverse the DataFrame order, sorting by date in descending order
    df.sort_index(ascending=False, inplace=True)

    price_col = df[column].values
    split_col = (df[splits_column] + 1.).values
    dividend_col = df[dividends_column].values
    adj_price_col = np.zeros(len(df.index))
    adj_price_col[0] = price_col[0]

    for i in range(1, len(price_col)):
        val = adj_price_col[i - 1] + adj_price_col[i - 1] * (
            ((price_col[i] * split_col[i - 1]) - price_col[i - 1] - dividend_col[i - 1]) / price_col[i - 1])
        adj_price_col[i] = round(val, 2)

    df[adj_column] = adj_price_col

    return df


class progress_bar_mine:
    progress_bar = ProgressBar(
        widgets=[Bar(marker='=', left='[', right=']')], maxval=100)

    def __init__(self, max_val, widgets=None, percentage=True, eta=True, transfer_speed=True):
        if widgets == None:
            widgets = [Bar(marker='=', left='[', right=']')]
        if percentage:
            widgets.append(' ')
            widgets.append(Percentage())
        if eta:
            widgets.append(' ')
            widgets.append(ETA())
        if transfer_speed:
            widgets.append(' ')
            widgets.append(FileTransferSpeed())
        self.progress_bar = ProgressBar(widgets=widgets, maxval=max_val)

    def start(self, label=None):
        if label:
            print('// ---------- ' + label + ' ---------- \\\\')
        self.progress_bar.start()

    def update(self, i):
        self.progress_bar.update(int(i))

    def finish(self):
        self.progress_bar.finish()
