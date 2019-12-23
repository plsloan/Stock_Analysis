import numpy


def getSMA(data, span, get_last=False):
    if get_last:
        return data['Close'].mean()
    else:
        return data['Close'].rolling(span, min_periods=1).mean()


def getEMA(data, span, get_last=False):
    if get_last:
        return data['Close'].ewm(span=span, min_periods=0, adjust=False, ignore_na=True).mean().iloc[-1]
    else:
        return data['Close'].ewm(span=span, min_periods=0, adjust=False, ignore_na=True).mean()


def getMomentum(data, span):
    return data['Close'].iloc[-1]/data['Close'].iloc[-(span+1)] - 1


def getRSI(data):
    series = data['Close']
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
    data_bollinger = data['Close'].rolling(window=w)
    center = data_bollinger.mean()
    upper = data_bollinger.mean() + data_bollinger.std() * x
    lower = data_bollinger.mean() - data_bollinger.std() * x
    return upper, center, lower


def getMACD(data):
    macd = getEMA(data, 12) - getEMA(data, 26)
    sig = macd.ewm(span=9, min_periods=0, adjust=False, ignore_na=True).mean()
    return macd, sig


def get_daily_returns(data):
    return (data/data.shift(1)) - 1


def get_cumulative_returns(data):
    return (data.iloc[-1]/data.iloc[0]) - 1
