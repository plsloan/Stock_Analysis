from db.connect import db
from iexfinance.refdata import get_symbols
from my_enums import Exchange, LearnerColumn, LearnerDataColumn, StockColumn, StockRecordsColumn
from yfinance import Ticker
import json
import pandas as pd
import numpy as np


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


def get_stock_symbols():
    return db.Stocks.distinct('Symbol')


def initialize_stocks():
    '''Clear and initialize database.'''
    # Clear db.Stocks
    db.Stocks.delete_many({})
    # Insert exchange, symbol, and name for stocks
    for s in get_symbols():
        db.Stocks.insert_one({
            StockColumn.Exchange.name: s['exchange'],
            StockColumn.Symbol.name: s['symbol'],
            StockColumn.Name.name: s['name'],
            StockColumn.Records.name: []
        })
    # Remove all with exchanges that are not Nasdaq or NYSE
    db.Stocks.delete_many({
        StockColumn.Exchange.name: {
            '$nin': [
                Exchange.Nasdaq.value,
                Exchange.Nyse.value
            ]
        }
    })
    if len(db.Stocks.find_one({StockColumn.Symbol.name: "SPY"})) == 0:
        db.Stocks.insert_one({
            StockColumn.Exchange.name: 'NYS',
            StockColumn.Symbol.name: 'SPY',
            StockColumn.Name.name: 'S&P 500',
            StockColumn.Records.name: []
        })


def initialize_learners():
    '''Clear and initialize learners'''
    from bson.binary import Binary
    import pickle

    db.Learners.delete_many({})
    db.QTable.delete_many({})
    db.RTable.delete_many({})
    db.TTable.delete_many({})
    num_indicators = 2
    num_states = (int)('9'*num_indicators)
    num_actions = 3
    for s in get_stock_symbols():
        db.Learners.insert_one({
            LearnerColumn.Symbol.name: s,
            LearnerColumn.Data.name: {
                LearnerDataColumn.bins.name: 8,
                LearnerDataColumn.impact.name: 0.0,
                LearnerDataColumn.verbose.name: False,
                LearnerDataColumn.alpha.name: 0.2,
                LearnerDataColumn.dyna.name: 200,
                LearnerDataColumn.gamma.name: 0.9,
                LearnerDataColumn.num_actions.name: num_actions,
                LearnerDataColumn.num_states.name: num_states,
                LearnerDataColumn.radr.name: 0.99,
                LearnerDataColumn.rar.name: 0.5,
                LearnerDataColumn.a.name: 0,
                LearnerDataColumn.s.name: 0
            }
        })
        db.QTable.insert_one({
            LearnerColumn.Symbol.name: s,
            LearnerDataColumn.Q.name: [[0] * num_states] * num_actions
        })
        db.RTable.insert_one({
            LearnerColumn.Symbol.name: s,
            LearnerDataColumn.R.name: [[0] * num_states] * num_actions
        })
        db.TTable.insert_one({
            LearnerColumn.Symbol.name: s,
            LearnerDataColumn.T.name: [
                [[0] * num_states] * num_actions] * num_states
        })


def load_learners():
    from strategy_learner import StrategyLearner

    documents = db.Learners.find({})
    learners = []
    for d in documents:
        data = d[LearnerColumn.Data.name]
        this_learner = StrategyLearner(
            bins=data[LearnerDataColumn.bins.name],
            impact=data[LearnerDataColumn.impact.name],
            verbose=data[LearnerDataColumn.verbose.name],
            alpha=data[LearnerDataColumn.alpha.name],
            dyna=data[LearnerDataColumn.dyna.name],
            gamma=data[LearnerDataColumn.gamma.name],
            num_actions=data[LearnerDataColumn.num_actions.name],
            num_states=data[LearnerDataColumn.num_states.name],
            rar=data[LearnerDataColumn.rar.name],
            radr=data[LearnerDataColumn.radr.name]
        )
        this_learner.learner.a = data[LearnerDataColumn.a.name]
        this_learner.learner.s = data[LearnerDataColumn.s.name]
        this_learner.learner.Q = data[LearnerDataColumn.Q.name]
        this_learner.learner.R = data[LearnerDataColumn.R.name]
        this_learner.learner.T = data[LearnerDataColumn.T.name]
        this_learner.learner.verbose = data[LearnerDataColumn.verbose.name]
        learners.append(this_learner)
    return learners


def print_stocks(exchange=None):
    '''Print all stocks from exchange.
    If no exchange is given, it prints all stocks.

    Parameters
    ----------
        exchange (optional)
    '''
    if exchange:
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
    del df[StockColumn._id.name]
    return df


def update_stock_records():
    '''Update all stock records from Yahoo API.'''
    from utils import convert_dataframe_to_document

    for sym in get_stock_symbols():
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
