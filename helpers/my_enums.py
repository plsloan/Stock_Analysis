from enum import Enum


class Exchange(Enum):
    Nasdaq = 'NASDAQ'
    NewYorkStockExchange = 'NYSE'


class StockColumn(Enum):
    _id = 0
    Exchange = 1
    Symbol = 2
    Name = 3
    Records = 4


class StockRecordsColumn(Enum):
    AdjustedClose = 0
    BollingerBand_Center = 1
    BollingerBand_Lower = 2
    BollingerBand_Upper = 3
    BollingerPercentage = 4
    Close = 5
    Date = 6
    Dividends = 7
    EMA_20 = 8
    EMA_5 = 9
    EMA_50 = 10
    High = 11
    Low = 12
    MACD_Signal = 13
    MACD_Value = 14
    Open = 15
    Price_EMA_Ratio = 16
    Price_SMA_Ratio = 17
    SMA_20 = 18
    SMA_5 = 19
    SMA_50 = 20
    StochasticBands = 21
    StockSplits = 22
    Volume = 23
