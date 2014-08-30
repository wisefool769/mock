import random
import datetime
import math
from ystockquote import get_historical_prices
from numpy import std, array
from calc import two_digit_str


def get_tickers(n, start_yyyymmdd, end_yyyymmdd = None):
    if not end_yyyymmdd:
        today = datetime.datetime.now()
        end_yyyymmdd = str(today.year) + "-" + two_digit_str(today.month) + "-" + two_digit_str(today.day)
    with open("sp500.txt", "r") as rf:
        tickers = rf.read().replace("\r", "").split("\n")
    n_tickers = random.sample(tickers, n)
    prices = get_prices(n_tickers, start_yyyymmdd, end_yyyymmdd)
    bsm_params = get_bsm_params(prices)
    return bsm_params

def order_dates(yyyymmdd):
    year, month, day = yyyymmdd.split("-")
    return (year, month, day)

def get_prices(tickers, start_yyyymmdd, end_yyyymmdd):
    symbols = dict()
    for symbol in tickers:
        all_prices = get_historical_prices(symbol, start_yyyymmdd, end_yyyymmdd)
        price_dates = sorted(all_prices.keys(), key=lambda k: order_dates(k))
        close_prices = [float(all_prices[d]["Adj Close"]) for d in price_dates]
        symbols[symbol] = close_prices
    return symbols

def get_bsm_params(prices):
    days_in_years = 252.0
    params = dict()
    for symbol in prices:
        params[symbol] = dict()
        params[symbol]["spot"] = prices[symbol][-1]
        log_prices = [math.log(p) for p in prices[symbol]]
        log_returns = [j-i for i, j in zip(log_prices[:-1], log_prices[1:])]
        params[symbol]["volatility"] = std(array(log_returns)) * math.sqrt(days_in_years)
        # CBOE has set rules on strike increments based on stock price
        # 2.50 for stocks below $25
        if params[symbol]["spot"] < 25:
            params[symbol]["strike_increments"] = 2.50
        # 5.00 for stocks from $25 to $200
        elif params[symbol]["spot"] <= 200:
            params[symbol]["strike_increments"] = 5.00
        # 10.00 for stocks above $200
        else:
            params[symbol]["strike_increments"] = 10.00
    return params




