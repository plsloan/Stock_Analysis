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
    RecordIds = 4
    LearnerId = 5


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


class LearnerColumn(Enum):
    Symbol = 0
    Data = 1


class LearnerDataColumn(Enum):
    # Strategy Learner
    alpha = 0
    bins = 1
    dyna = 2
    gamma = 3
    impact = 4
    num_actions = 5
    num_states = 6
    radr = 7
    rar = 8
    verbose = 9

    # QLearner
    a = 10
    s = 11
    Q = 12
    R = 13
    T = 14
