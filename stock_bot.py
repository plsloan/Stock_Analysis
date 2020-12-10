from datetime import datetime as dt
import numpy as np
import pandas as pd

from db.connect import db
from db.utils import initialize_stocks, initialize_learners, load_learners
from utils import run_stock_bot


def main():
    if db.Stocks.count_documents({}) == 0:
        initialize_stocks()

    if db.Learners.count_documents({}) == 0:
        initialize_learners()

    # learners = load_learners()

    run_stock_bot()


# -------------- MAIN ------------- #

if (__name__ == '__main__'):
    main()
