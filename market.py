# market.py
import os, time
import params as p
import re
from math import exp, sqrt
from numpy.random import normal, gamma
from time import time
from calc import isfloat, contains_substring, which_substring

fname = "orders.txt"

class Stock:
    def __init__(self, S, mu, sigma):
        self.price = S
        self.drift = mu
        self.vol = sigma

    def update_price(self, time_in_seconds):
        t = time_in_seconds * p.seconds_to_years
        mean = self.drift * t
        sdev = self.vol * sqrt(t)
        log_return = normal(loc=mean, scale=sdev)
        self.price *= exp(log_return)

    def set_price(self, S):
        self.price = S

def risk_reversal(order):
    split_order = order.split(" ")
    months_order = [m for m in split_order if m in p.months]
    strikes = [float(k) for k in split_order if isfloat(k)]
    # calls over situations
    # if contains_substring(order, p.calls_over):
    #     continue



def run_mock():
    S = Stock(p.initial_spot, p.stock_drift, p.stock_vol)
    while True:
        dt = gamma(shape=p.time_shape, scale=p.time_scale)
        start_time = time()
        while (time() - start_time < dt):
            if os.path.isfile(fname):
                with open(fname, "r") as f:
                    orders = f.readlines()
                    for o in orders:
                        print(o)
                os.remove(fname)
        S.update_price(dt)
        print(S.price)


if __name__ == "__main__":
    run_mock()
