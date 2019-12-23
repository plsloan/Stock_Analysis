import numpy as np


def getSMA(data, span, get_last=False):
    if get_last:
        return data['Adjusted Close'].mean()
    else:
        return data['Adjusted Close'].rolling(span, min_periods=1).mean()


def getEMA(data, span, get_last=False):
    if get_last:
        return data['Adjusted Close'].ewm(span=span, min_periods=0, adjust=False, ignore_na=True).mean().iloc[-1]
    else:
        return data['Adjusted Close'].ewm(span=span, min_periods=0, adjust=False, ignore_na=True).mean()


def getMomentum(data, span):
    return data['Adjusted Close'].iloc[-1]/data['Adjusted Close'].iloc[-(span+1)] - 1


def getRSI(data):
    series = data['Adjusted Close']
    period = 14
    delta = series.diff().dropna()
    if (len(series) >= 14):
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        # first value is sum of avg gains
        u[u.index[period-1]] = numpy.mean(u[:period])
        u = u.drop(u.index[:(period-1)])
        # first value is sum of avg losses
        d[d.index[period-1]] = numpy.mean(d[:period])
        d = d.drop(d.index[:(period-1)])
        rs = u.ewm(com=period-1, adjust=False).mean() / \
            d.ewm(com=period-1, adjust=False).mean()
        return (100 - 100 / (1 + rs)).iloc[-1]
    else:
        return 100


def getBollingerBand(data):
    w = 20  # span
    x = 2   # standard deviation periods
    data_bollinger = data['Adjusted Close'].rolling(window=w)
    center = data_bollinger.mean()
    upper = data_bollinger.mean() + data_bollinger.std() * x
    lower = data_bollinger.mean() - data_bollinger.std() * x
    return upper, center, lower


def getMACD(data):
    macd = getEMA(data, 12) - getEMA(data, 26)
    sig = macd.ewm(span=9, min_periods=0, adjust=False, ignore_na=True).mean()
    return macd, sig


def price_sma_ratio(data):
    return data['Adjusted Close'] / getSMA(data, 20)
    


def price_ema_ratio(data):
    return data['Adjusted Close'] / getEMA(data, 20)
     


def bollinger_percentage(data):
    upper, center, lower = getBollingerBand(data)
    percentage = np.abs((data['Adjusted Close'].dropna() - lower.dropna()) /
                        (upper.dropna() - lower.dropna()))
    return percentage.sort_index(ascending=False) * 100


def stochastic_band(data):
    return data['Adjusted Close'].rolling(14).apply(
        lambda x: 100 * ((x[-1] - x.min()) / (x.max() - x.min())))


def get_daily_returns(data):
    return (data/data.shift(1)) - 1


def get_cumulative_returns(data):
    return (data.iloc[-1]/data.iloc[0]) - 1
