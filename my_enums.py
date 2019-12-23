from enum import Enum


class Exchange(Enum):
    AmericanStockExchange = 'ASE'
    Bats = 'BATS'
    Nasdaq = 'NAS'
    Nyse = 'NYS'
    OverTheCounter = 'OTC'
    PacificStockExchange = 'PSE'


class StockColumn(Enum):
    _id = 0
    Exchange = 1
    Symbol = 2
    Name = 3
    Records = 4


class StockRecordsColumn(Enum):
    Date = 0
    Open = 1
    Close = 2
    High = 3
    Low = 4
    Volume = 5
    Dividends = 6
    StockSplits = 7
    AdjustedClose = 8
    SMA_5 = 9
    SMA_20 = 10
    SMA_50 = 11
    EMA_5 = 12
    EMA_20 = 13
    EMA_50 = 14
    BollingerBand_Upper = 15
    BollingerBand_Center = 16
    BollingerBand_Lower = 17
    MACD_Value = 18
    MACD_Signal = 19
    Price_SMA_Ratio = 20
    Price_EMA_Ratio = 21
    BollingerPercentage = 22
    StochasticBands = 23
