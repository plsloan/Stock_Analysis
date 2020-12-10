"""
An improved version of your marketsim code that accepts 
a "trades" data frame (instead of a file). 

More info on the trades data frame below. 

It is OK not to submit this file if you have subsumed 
its functionality into one of your other required code files.

Student Name: Phillip Sloan (replace with your name)
GT User ID: psloan31 (replace with your User ID)
GT ID: 903452647 (replace with your GT ID)
"""

from db.utils import get_data
import pandas as pd
import numpy as np
import datetime as dt


def compute_portvals(trades_df, start_date, end_date, start_val=100000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    trades_df = trades_df.loc[start_date:end_date]
    trades_df = trades_df.sort_index()
    symbols = list(trades_df.keys().unique())
    symbols.remove('cash')

    prices_df = get_data(symbols, pd.date_range(
        start_date, end_date))[symbols]
    prices_df['cash'] = 1.0
    symbols.append('cash')

    holdings_df = pd.DataFrame(data=np.zeros(
        (trades_df.shape[0], prices_df.shape[1])), columns=prices_df.keys(), index=trades_df.index)
    holdings_df.iloc[0][-1] = start_val
    holdings_df.iloc[0] = holdings_df.iloc[0] + trades_df.iloc[0]
    for i in range(1, len(trades_df)):
        holdings_df.iloc[i] = holdings_df.iloc[i-1] + trades_df.iloc[i]

    values_df = pd.DataFrame(data=np.zeros(
        (prices_df.shape[0], prices_df.shape[1])), columns=prices_df.keys(), index=prices_df.index)
    holdings_merged = holdings_df.loc[~holdings_df.index.duplicated(
        keep='last')]
    last_index = -1
    for index in values_df.index.values:
        index = pd.to_datetime(index).strftime('%Y-%m-%d')
        prices = prices_df.loc[index]
        if np.datetime64(index) in holdings_merged.index.values:
            values_df.loc[index] = prices * holdings_merged.loc[index]
            last_index = index
        else:
            if last_index != -1:
                values_df.loc[index] = prices * \
                    holdings_merged.loc[last_index]

    portvals_df = values_df.sum(axis=1)
    portvals_df.loc[portvals_df.index < trades_df.index[0]] = start_val
    rv = pd.DataFrame(index=portvals_df.index,
                      data=portvals_df.values, columns=['portvals'])

    return rv


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    symbol = 'JPM'
    start = dt.datetime(2008, 1, 1)
    end = dt. datetime(2009, 12, 31)

    prices_df = get_data([symbol], pd.date_range(start, end))
    prices_df['cash'] = 1.0
    prices_df.sort_index()

    start_val = 100000
    in_start = dt.datetime(2008, 1, 1)
    in_end = dt.datetime(2009, 12, 31)
    out_start = dt.datetime(2010, 1, 1)
    out_end = dt.datetime(2011, 12, 31)

    spy = get_data(['SPY'], pd.date_range(in_start, out_end))
    orders_df = pd.DataFrame(index=spy.index, columns=[
                             'Symbol', 'Order', 'Shares'])
    orders_df.iloc[0] = ['SPY', 'BUY', 1000]
    orders_df.dropna(inplace=True)

    symbols = list(orders_df['Symbol'].unique())

    trades_df = pd.DataFrame(data=np.zeros(
        (orders_df.shape[0], prices_df.shape[1])), columns=prices_df.keys(), index=orders_df.index)
    for i in range(len(orders_df)):
        insert = np.zeros(len(prices_df.keys()))
        d = orders_df.index[i]._date_repr
        s = symbols.index(orders_df.iloc[i]['Symbol'])
        if orders_df.iloc[i]['Order'].lower().strip() == 'buy':
            insert[s] = orders_df.iloc[i]['Shares']
            insert[-1] = orders_df.iloc[i]['Shares'] * \
                prices_df.loc[d][s] * -1
        elif orders_df.iloc[i]['Order'].lower().strip() == 'sell':
            insert[s] = orders_df.iloc[i]['Shares'] * -1
            insert[-1] = orders_df.iloc[i]['Shares'] * \
                prices_df.loc[d][s]
        trades_df.iloc[i] = insert

    # Process orders
    portvals = compute_portvals(trades_df, in_start, out_end)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # portfolio
    cum_ret = portvals[-1] / portvals[0] - 1
    daily_ret = (portvals / portvals.shift(1) - 1)[1:]
    avg_daily_ret = daily_ret.mean()
    std_daily_ret = daily_ret.std()
    sharpe_ratio = avg_daily_ret / std_daily_ret * np.sqrt(252)

    cum_ret_SPY = spy.iloc[-1] / spy.iloc[0] - 1
    daily_ret_SPY = (spy / spy.shift(1) - 1)[1:]
    avg_daily_ret_SPY = daily_ret_SPY.mean()
    std_daily_ret_SPY = daily_ret_SPY.std()
    sharpe_ratio_SPY = avg_daily_ret_SPY / std_daily_ret_SPY * np.sqrt(252)

    # Compare portfolio against $SPX
    content = ''
    content = content + "Date Range: {} to {}".format(in_start, out_end) + '\n'
    content = content + '\n'
    content = content + "Sharpe Ratio of Fund: {}".format(sharpe_ratio) + '\n'
    content = content + \
        "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY[0]) + '\n'
    content = content + '\n'
    content = content + "Cumulative Return of Fund: {}".format(cum_ret) + '\n'
    content = content + \
        "Cumulative Return of SPY : {}".format(cum_ret_SPY[0]) + '\n'
    content = content + '\n'
    content = content + \
        "Standard Deviation of Fund: {}".format(std_daily_ret) + '\n'
    content = content + \
        "Standard Deviation of SPY : {}".format(std_daily_ret_SPY[0]) + '\n'
    content = content + '\n'
    content = content + \
        "Average Daily Return of Fund: {}".format(avg_daily_ret) + '\n'
    content = content + \
        "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY[0])

    print(content)


if __name__ == "__main__":
    # for i in range(1, 13):
    #     if i < 10:
    #         test_code(orders_file='./orders/orders-0' + str(i) + '.csv')
    #         print('\n\n\n\n')
    #     else:
    #         test_code(orders_file='./orders/orders-' + str(i) + '.csv')
    #         print('\n\n\n\n')
    test_code()
