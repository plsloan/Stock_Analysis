from db_connect import db
from iexfinance.refdata import get_symbols
from my_enums import Exchange
from utils import convert_dataframe_to_document
from yfinance import Ticker

import json
import pandas as pd


def initialize_stocks():
    '''Clear and initialize database.'''
    # Clear db.Stocks
    db.Stocks.delete_many({})
    # Insert exchange, symbol, and name for stocks
    for s in get_symbols():
        db.Stocks.insert_one({
            'Exchange': s['exchange'],
            'Symbol': s['symbol'],
            'Name': s['name'],
            'Records': []
        })
    # Remove all with exchanges that are not Nasdaq or NYSE
    db.Stocks.delete_many({
        'Exchange': {
            '$nin': [
                Exchange.Nasdaq.value[0],
                Exchange.Nyse.value[0]
            ]
        }
    })


def update_stock_records():
    '''Update all stock records from Yahoo API.'''
    symbols = db.Stocks.distinct('Symbol')
    for sym in symbols:
        try:
            stock = Ticker(sym).history(period='1y')
            db.Stocks.update_one(
                {'Symbol': sym},
                {'$set': {'Records': convert_dataframe_to_document(stock)}}
            )
        except:
            db.Stocks.update_one(
                {'Symbol': sym},
                {'$set': {'Records': []}}
            )


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
            {'$set': {'Records': []}}
        )
        print('Cleared stock records.\n')
    except:
        print('An error occurred when clearing stock records.\n')


def print_stocks(exchange=None):
    '''Print all stocks from exchange.
    If no exchange is given, it prints all stocks.

    Parameters
    ----------
        exchange (optional)
    '''
    if exchange:
        stocks = db.Stocks.find({'Exchange': exchange.value})
        print('\n' + exchange.name)
        print('---------------------\n')
        for s in stocks:
            print(s['Symbol'] + ' - ' + s['Name'])
    else:
        for exchange in Exchange:
            stocks = db.Stocks.find({'Exchange': exchange.value})
            print('\n' + exchange.name)
            print('---------------------\n')
            for s in stocks:
                print(s['Symbol'] + ' - ' + s['Name'])


def query_as_dataframe(query_results):
    '''
    Parameters
    ----------
        query_results
            results from mongodb query
            example - db.Stocks.find({})

    Returns
    -------
        df
            query_results as pandas DataFrame
    '''
    df = pd.DataFrame(list(query_results))
    del df['_id']
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
    records = df[df[col] == value]['Records']
    if len(records) == 1:
        return pd.DataFrame(records.iloc[0])
    elif len(records) == 0:
        print('No stocks were matched.')
    else:
        print('More than one stock was matched.')
