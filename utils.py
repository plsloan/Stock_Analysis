from get_indicators import getSMA, getEMA, getBollingerBand, getMACD, price_sma_ratio, price_ema_ratio, bollinger_percentage, stochastic_band
from my_enums import StockColumn, StockRecordsColumn
from progressbar import ProgressBar, Bar, Percentage, ETA, FileTransferSpeed
import numpy as np


def calculate_adjusted_prices(df):
    """ Vectorized approach for calculating the adjusted prices for the
    specified column in the provided DataFrame. This creates a new column
    called 'adj_<column name>' with the adjusted prices. This function requires
    that the DataFrame have columns with dividend and split_ratio values.


    :param df: DataFrame with raw prices along with dividend and split_ratio
        values
    :return: DataFrame with the addition of the adjusted price column
    """
    column = StockRecordsColumn.Close.name
    adj_column = StockRecordsColumn.AdjustedClose.name
    dividends_column = StockRecordsColumn.Dividends.name
    splits_column = StockRecordsColumn.StockSplits.name

    # Reverse the DataFrame order, sorting by date in descending order
    df.sort_index(ascending=False, inplace=True)

    price_col = df[column].values
    split_col = (df['Stock Splits'] + 1.).values
    dividend_col = df[dividends_column].values
    adj_price_col = np.zeros(len(df.index))
    adj_price_col[0] = price_col[0]

    for i in range(1, len(price_col)):
        val = adj_price_col[i - 1] + adj_price_col[i - 1] * (
            ((price_col[i] * split_col[i - 1]) - price_col[i - 1] - dividend_col[i - 1]) / price_col[i - 1])
        adj_price_col[i] = round(val, 2)

    df[adj_column] = adj_price_col

    return df


def convert_dataframe_to_document(df):
    df = calculate_adjusted_prices(df)

    # add SMAs
    df[StockRecordsColumn.SMA_5.name] = getSMA(df, 5)
    df[StockRecordsColumn.SMA_20.name] = getSMA(df, 20)
    df[StockRecordsColumn.SMA_50.name] = getSMA(df, 50)

    # add EMAs
    df[StockRecordsColumn.EMA_5.name] = getEMA(df, 5)
    df[StockRecordsColumn.EMA_20.name] = getEMA(df, 20)
    df[StockRecordsColumn.EMA_50.name] = getEMA(df, 50)

    # add bollinger bands
    upper, center, lower = getBollingerBand(df)
    df[StockRecordsColumn.BollingerBand_Upper.name] = upper
    df[StockRecordsColumn.BollingerBand_Center.name] = center
    df[StockRecordsColumn.BollingerBand_Lower.name] = lower

    # add MACD
    macd, signal = getMACD(df)
    df[StockRecordsColumn.MACD_Value.name] = macd
    df[StockRecordsColumn.MACD_Signal.name] = signal

    # price ratios
    df[StockRecordsColumn.Price_SMA_Ratio.name] = price_sma_ratio(df)
    df[StockRecordsColumn.Price_EMA_Ratio.name] = price_ema_ratio(df)

    # add bollinger percentage
    df[StockRecordsColumn.BollingerPercentage.name] = bollinger_percentage(df)

    df[StockRecordsColumn.StochasticBands.name] = stochastic_band(df)

    document = []
    for i in range(len(df)):
        record = {}
        record[StockRecordsColumn.Date.name] = str(df.iloc[i].name)[:-9]
        for k in df.keys():
            record[k] = df.iloc[i][k]
        document.append(record)
    return document


def get_command():
    return strip_string(input('StockBot: ').lower())


def strip_string(s):
    return s.replace(' ', '').replace('\t', '')


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
