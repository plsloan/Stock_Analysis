from db.utils import get_data
from marketsimcode import compute_portvals
from helpers.QLearner import QLearner
from helpers.get_indicators import get_daily_returns, price_sma_ratio, price_ema_ratio, bollinger_percentage, stochastic_band

import datetime as dt
import numpy as np
import pandas as pd
import random


class StrategyLearner(object):

    # constructor
    def __init__(self, num_states=9999, num_actions=3, alpha=0.2,
                 gamma=0.9, rar=0.5, radr=0.99, dyna=200, verbose=False, impact=0.0, bins=8):
        self.bins = bins
        self.impact = impact
        self.verbose = verbose
        self.learner = QLearner(num_states=9999, num_actions=3,
                                dyna=dyna, alpha=alpha, gamma=gamma, rar=rar, radr=radr)

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=10000, iterations=5, impact=0.0):
        dates = pd.date_range(sd, ed)
        prices_sym = get_data(symbol, dates)
        prices_spy = get_data('SPY', dates)
        daily_returns = get_daily_returns(prices_sym)
        if self.verbose:
            print(prices_sym)

        # state stats
        sma_ratio = pd.DataFrame()
        ema_ratio = pd.DataFrame()
        boll_percentage = pd.DataFrame()
        stochastic = pd.DataFrame()

        sma_ratio['sma_ratio'] = price_sma_ratio(prices_sym)
        ema_ratio['ema_ratio'] = price_ema_ratio(prices_sym)
        boll_percentage['boll_percentage'] = bollinger_percentage(prices_sym)
        stochastic['stochastic'] = stochastic_band(prices_sym)

        factors = sma_ratio.join([ema_ratio, boll_percentage, stochastic])
        factors.dropna(inplace=True)

        # strip down prices
        prices_sym = prices_sym.loc[factors.index]
        prices_spy = prices_spy.loc[factors.index]

        ints = []
        thresholds = []
        for f in factors:
            intervals = pd.qcut(
                factors[f], self.bins, retbins=True, duplicates='drop')
            ints.append(np.digitize(factors[f].round(3), intervals[1]))
            thresholds.append(intervals)

        ints = np.array(ints, dtype=str).T
        thresholds = np.array(thresholds)
        states = map(lambda row: int(''.join(row)), ints)

        # learning cycle
        for i in range(iterations):
            trades_df = pd.DataFrame(index=prices_sym.index, columns=[symbol])
            a = self.learner.query_set_state(states[0])
            trades_df = self.handleAction(
                a, trades_df, symbol, prices_sym.index[0])
            len_states = len(states)
            long_rewards = (
                prices_sym / prices_sym.shift(1) - 1) * (1 - impact)
            short_rewards = (prices_sym.shift(
                1) / prices_sym - 1) * (1 - impact)
            for s in range(1, len_states):
                shares = getShares(trades_df.dropna())
                if shares == 0:  # not in market
                    r = 0
                elif shares > 0:  # long
                    r = long_rewards.iloc[s]
                elif shares < 0:  # short
                    r = short_rewards.iloc[s]
                a = self.learner.query(states[s], r)
                trades_df = self.handleAction(
                    a, trades_df, symbol, prices_sym.index[s])

        trades_df[pd.isnull(trades_df)] = 0
        return trades_df

    def testPolicy(self, symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=10000):
        # here we build a fake set of trades
        # your code should return the same sort of data
        # self.learner.rar = 0
        dates = pd.date_range(sd, ed)
        prices_sym = get_data(symbol, dates)
        prices_spy = get_data('SPY', dates)

        # state stats
        sma_ratio = pd.DataFrame()
        ema_ratio = pd.DataFrame()
        boll_percentage = pd.DataFrame()
        stochastic = pd.DataFrame()

        sma_ratio['sma_ratio'] = price_sma_ratio(prices_sym)
        ema_ratio['ema_ratio'] = price_ema_ratio(prices_sym)
        boll_percentage['boll_percentage'] = bollinger_percentage(prices_sym)
        stochastic['stochastic'] = stochastic_band(prices_sym)

        factors = sma_ratio.join([ema_ratio, boll_percentage, stochastic])
        factors.dropna(inplace=True)

        # strip down prices
        prices_sym = prices_sym.loc[factors.index]
        prices_spy = prices_spy.loc[factors.index]

        ints = []
        thresholds = []
        for f in factors:
            intervals = pd.qcut(
                factors[f], self.bins, retbins=True, duplicates='drop')
            ints.append(np.digitize(factors[f].round(3), intervals[1]))
            thresholds.append(intervals)

        ints = np.array(ints, dtype=str).T
        thresholds = np.array(thresholds)
        states = map(lambda row: int(''.join(row)), ints)

        # learning cycle
        trades_df = pd.DataFrame(index=prices_sym.index, columns=[symbol])
        len_states = len(states)
        long_rewards = prices_sym / prices_sym.shift(1) - 1
        short_rewards = prices_sym.shift(1) / prices_sym - 1
        for s in range(len_states):
            shares = getShares(trades_df.dropna())
            if shares == 0 or s == 0:  # not in market
                r = 0
            elif shares > 0:  # long
                r = long_rewards.iloc[s]
            elif shares < 0:  # short
                r = short_rewards.iloc[s]
            a = self.learner.query(states[s], r, update=False)
            trades_df = self.handleAction(
                a, trades_df, symbol, prices_sym.index[s])

        trades_df[pd.isnull(trades_df)] = 0
        return trades_df

    def handleAction(self, action, trades, symbol, loc):
        trades_df = trades.copy()
        if action == 0:
            if getShares(trades_df.dropna()) < 1000:
                trades_df.loc[loc] = 1000  # buy
        elif action == 1:
            if getShares(trades_df.dropna()) > -1000:
                trades_df.loc[loc] = -1000  # sell
        elif action == 2:
            trades_df.loc[loc] = 0  # nothing
        else:
            print("Invalid action...")
        return trades_df

    def benchmark(self, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000, impact=0.0):
        prices_df = get_data(symbol, pd.date_range(sd, ed))
        prices_df['cash'] = 1.0
        prices_df.sort_index()

        in_start = dt.datetime(2008, 1, 1)
        in_end = dt.datetime(2009, 12, 31)
        out_start = dt.datetime(2010, 1, 1)
        out_end = dt.datetime(2011, 12, 31)

        # prices
        in_sample = prices_df.loc[in_start:in_end][symbol]
        out_sample = prices_df.loc[out_start:out_end][symbol]
        symbol_prices = prices_df[symbol]
        spy_prices = prices_df['SPY']

        trades_df = pd.DataFrame(
            index=prices_df.index, columns=[symbol, 'cash'])

        trades_df.iloc[0] = 1000
        trades_df.iloc[1:] = 0
        rv = compute_portvals(trades_df, sd, ed, impact=impact)
        return rv


def getShares(orders):
    if len(orders) > 0:
        return orders.sum().iloc[-1]
    else:
        return 0


def addCashColumn(trades_df, prices_df, impact, symbol):
    buy_indices = trades_df[trades_df > 0].index
    sell_indices = trades_df[trades_df < 0].index
    trades_df['cash'] = 0
    trades_df.loc[buy_indices]['cash'] = -1 * trades_df[symbol].loc[buy_indices] * \
        prices_df[symbol].loc[buy_indices] * (1 + impact)  # add cash column
    trades_df.loc[sell_indices]['cash'] = -1 * trades_df[symbol].loc[sell_indices] * \
        prices_df[symbol].loc[sell_indices] * (1 - impact)
    return trades_df


if __name__ == "__main__":
    start_train = dt.datetime(2008, 1, 1)
    end_train = dt.datetime(2009, 12, 31)
    start_test = dt.datetime(2010, 1, 1)
    end_test = dt.datetime(2011, 12, 31)

    start = start_train
    end = end_train
    impact = 0.0
    symbol = 'JPM'

    prices_df = get_data(symbol, pd.date_range(start_train, end_train))

    learner = StrategyLearner(dyna=200, bins=5)

    train_trades = learner.addEvidence(
        iterations=10, sd=start_train, ed=end_train)
    train_trades = addCashColumn(train_trades, prices_df, impact, symbol)

    prices_df = get_data(symbol, pd.date_range(start_test, end_test))

    test1_trades = learner.testPolicy(
        symbol=symbol, sd=start_test, ed=end_test)
    test1_trades = addCashColumn(test1_trades, prices_df, impact, symbol)

    test2_trades = learner.testPolicy(
        symbol=symbol, sd=start_test, ed=end_test)
    test2_trades = addCashColumn(test2_trades, prices_df, impact, symbol)

    portvals = compute_portvals(train_trades, start, end)
    benchmark = learner.benchmark('JPM', sd=start, ed=end)

    # portfolio
    cum_ret = round((portvals.iloc[-1] / portvals.iloc[0] - 1)[0], 5)
    daily_ret = (portvals / portvals.shift(1) - 1)[1:]
    avg_daily_ret = round((daily_ret.mean())[0], 5)
    std_daily_ret = round((daily_ret.std())[0], 5)
    sharpe_ratio = round(avg_daily_ret / std_daily_ret * np.sqrt(252), 5)

    cum_ret_benchmark = round(
        (benchmark.iloc[-1] / benchmark.iloc[0] - 1)[0], 5)
    daily_ret_benchmark = (benchmark / benchmark.shift(1) - 1)[1:]
    avg_daily_ret_benchmark = round(daily_ret_benchmark.mean()[0], 5)
    std_daily_ret_benchmark = round(daily_ret_benchmark.std()[0], 5)
    sharpe_ratio_benchmark = round(
        avg_daily_ret_benchmark / std_daily_ret_benchmark * np.sqrt(252), 5)

    # # Compare portfolio against $benchmark
    content = ''
    content = content + \
        "Date Range: {} to {}".format(start, end) + '\n'
    content = content + '\n'
    content = content + "Sharpe Ratio of Fund: {}".format(sharpe_ratio) + '\n'
    content = content + \
        "Sharpe Ratio of benchmark : {}".format(
            sharpe_ratio_benchmark) + '\n'
    content = content + '\n'
    content = content + "Cumulative Return of Fund: {}".format(cum_ret) + '\n'
    content = content + \
        "Cumulative Return of benchmark : {}".format(
            cum_ret_benchmark) + '\n'
    content = content + '\n'
    content = content + \
        "Standard Deviation of Fund: {}".format(std_daily_ret) + '\n'
    content = content + \
        "Standard Deviation of benchmark : {}".format(
            std_daily_ret_benchmark) + '\n'
    content = content + '\n'
    content = content + \
        "Average Daily Return of Fund: {}".format(avg_daily_ret) + '\n'
    content = content + \
        "Average Daily Return of benchmark : {}".format(
            avg_daily_ret_benchmark)

    print(content)
