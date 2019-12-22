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


# TODO
class StockRecordsColumn(Enum):
    Zero = 0
