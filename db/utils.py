from db.connect import db
from helpers.my_enums import Exchange, StockColumn, StockRecordsColumn
from pymongo import DESCENDING
from yfinance import Ticker
import pandas as pd


def delete_stocks():
    '''Deletes all stocks.'''
    try:
        db.Stocks.delete_many({})
        print('Cleared all stocks.\n')
    except:
        print('An error occurred when clearing stocks.\n')


def delete_stock_records():
    '''Sets Records to empty list for all stocks.'''
    try:
        db.Stocks.update_many(
            {},
            {'$set': {StockColumn.Records.name: []}}
        )
        print('Cleared stock records.\n')
    except:
        print('An error occurred when clearing stock records.\n')


def get_all_data(symbol, dates):
    stock = db.Stocks.find_one({StockColumn.Symbol.name: symbol})
    df = pd.DataFrame(stock[StockColumn.Records.name])
    df[StockRecordsColumn.Date.name] = df[StockRecordsColumn.Date.name].astype(
        'datetime64[ns]')
    indexed_df = df.set_index(StockRecordsColumn.Date.name)
    in_range_df = indexed_df.loc[indexed_df.index.isin(dates)]
    return in_range_df.sort_index(ascending=False)


def get_data(symbols, dates, addSPY=True, colname=StockRecordsColumn.AdjustedClose.name):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if addSPY and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = ['SPY'] + symbols

    for symbol in symbols:
        stock = db.Stocks.find_one({StockColumn.Symbol.name: symbol})
        df_temp = pd.DataFrame(stock[StockColumn.Records.name])
        df_temp[StockRecordsColumn.Date.name] = df_temp[StockRecordsColumn.Date.name].astype(
            'datetime64[ns]')
        indexed_df = df_temp.set_index(StockRecordsColumn.Date.name)
        in_range_df = indexed_df.loc[indexed_df.index.isin(dates)]
        sorted_df = in_range_df.sort_index(ascending=False)

        df[symbol] = sorted_df[colname]

        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df


def get_records_from_dataframe(df, col, value):
    '''
    Parameters
    ----------
        df
            pandas DataFrame
        col
            StockColumn name
        value
            value for Column lookup

    Returns
    -------
        records_df
    '''
    records = df[df[col] == value][StockColumn.Records.name]
    if len(records) == 1:
        return pd.DataFrame(records.iloc[0])
    elif len(records) == 0:
        print('No stocks were matched.')
    else:
        print('More than one stock was matched.')


def get_stock_dataframe():
    import requests
    url = 'https://financialmodelingprep.com/api/v3/search?apikey=741b15c92add15628eb47e3586e60b2c&query='
    result = requests.get(url)
    return pd.DataFrame(result.json())


def get_symbols():
    stock_df = get_stock_dataframe()
    return stock_df.sort_values('symbol')['symbol']


def get_symbols_db():
    return db.Stocks.distinct('Symbol')


def initialize_stocks():
    '''Clear and initialize database.'''
    # Clear db.Stocks
    db.Stocks.delete_many({})

    # Insert initial state for stocks
    for index, row in get_stock_dataframe().iterrows():
        if row['exchangeShortName'] and row['name'] and row['symbol'] and ('-' not in row['symbol'] or '.' not in row['symbol']):
            db.Stocks.insert_one({
                StockColumn.Exchange.name: row['exchangeShortName'].strip(),
                StockColumn.Name.name: row['name'].strip(),
                StockColumn.Symbol.name: row['symbol'].strip()
            })

    # Remove all with exchanges that are not Nasdaq or NYSE
    db.Stocks.delete_many({
        StockColumn.Exchange.name: {
            '$nin': [
                Exchange.Nasdaq.value,
                Exchange.NewYorkStockExchange.value
            ]
        }
    })

    if not db.Stocks.find_one({StockColumn.Symbol.name: "SPY"}):
        db.Stocks.insert_one({
            StockColumn.Exchange.name: Exchange.NewYorkStockExchange.value,
            StockColumn.Name.name: 'S&P 500',
            StockColumn.Symbol.name: 'SPY'
        })


def print_stocks(exchange=None):
    '''Print all stocks from exchange.
    If no exchange is given, it prints all stocks.

    Parameters
    ----------
        exchange (optional)
    '''
    if exchange is not None:
        stocks = db.Stocks.find({StockColumn.Exchange.name: exchange.value})
        print('\n' + exchange.name)
        print('---------------------\n')
        for s in stocks:
            print(s[StockColumn.Symbol.name] +
                  ' - ' + s[StockColumn.Name.name])
    else:
        for exchange in Exchange:
            stocks = db.Stocks.find(
                {StockColumn.Exchange.name: exchange.value})
            print('\n' + exchange.name)
            print('---------------------\n')
            for s in stocks:
                print(s[StockColumn.Symbol.name] +
                      ' - ' + s[StockColumn.Name.name])


def update_stock_records():
    '''Update all stock records from Yahoo API.'''
    from utils import convert_dataframe_to_document

    for sym in get_symbols_db():
        try:
            stock = Ticker(sym).history(period='1y')
            record_doc = convert_dataframe_to_document(stock)
            db.Stocks.update_one(
                {StockColumn.Symbol.name: sym},
                {'$set': {
                    StockColumn.Records.name: record_doc}}
            )
        except:
            db.Stocks.update_one(
                {StockColumn.Symbol.name: sym},
                {'$set': {StockColumn.Records.name: []}}
            )
