from datetime import datetime as dt
from db.connect import db
from db.utils import initialize_stocks, load_learners
import numpy as np
import pandas as pd
from utils import run_stock_bot


def main():
    if db.Stocks.count_documents({}) == 0:
        initialize_stocks()

    learners = load_learners()

    run_stock_bot()


# -------------- MAIN ------------- #

if (__name__ == '__main__'):
    main()
