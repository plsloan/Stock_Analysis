import numpy

def getSMA(data, span):
    return data['Close'].mean()
def getSMA_set(data, span):
    return data['Close'].rolling(span, min_periods=1).mean()
def getEMA(data, span):
    return data['Close'].ewm(span=span, min_periods=0, adjust=False, ignore_na=True).mean().iloc[-1]
def getEMA_set(data, span):
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
        u[u.index[period-1]] = numpy.mean( u[:period] ) #first value is sum of avg gains
        u = u.drop(u.index[:(period-1)])
        d[d.index[period-1]] = numpy.mean( d[:period] ) #first value is sum of avg losses
        d = d.drop(d.index[:(period-1)])
        rs = u.ewm(com=period-1, adjust=False).mean() / d.ewm(com=period-1, adjust=False).mean()
        return (100 - 100 / (1 + rs)).iloc[-1]
    else: 
        return 100
def getBollingerBand(data):
    s = 20  # span
    x = 2   # standard deviation periods
    data_bollinger = data['Close'].ewm(span=s, min_periods=0, adjust=False, ignore_na=True)
    center = data_bollinger.mean()
    upper = data_bollinger.mean() + data_bollinger.std() * x
    lower = data_bollinger.mean() - data_bollinger.std() * x
    return upper, center, lower
def getMACD(data):
    macd = getEMA_set(data, 12) - getEMA_set(data, 26)
    sig  = macd.ewm(span=9, min_periods=0, adjust=False, ignore_na=True).mean()
    return macd, sig