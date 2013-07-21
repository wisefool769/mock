################### OPTION.PY STARTS ###################
 
# option.py
import math
import random
from scipy.stats import norm
 
class Option:
    def __init__(self, spot, strike, vol, rate, time_to_exp):
        self.S = spot
        self.K = strike
        self.sigma = vol
        self.r = rate
        self.tau = time_to_exp
        self.interest = math.exp(self.r*self.tau)
        self.forward = self.K*self.interest
        self.rc = self.ATFrc()
        self.C = self.bsm()
        self.P = self.pcp()

    def bsm(self):
        # returns the Black-Scholes Merton value of
        # the call from option's parameters
        vol_adj_time = self.sigma*math.sqrt(self.tau)
        pv_strike = self.K*math.exp(-1*self.r*self.tau)
        d1 = 1/vol_adj_time*(math.log(self.S/self.K) + (self.r + self.sigma ** 2 / 2)*math.sqrt(self.tau))
        d2 = d1 - vol_adj_time
        return norm.cdf(d1)*self.S - norm.cdf(d2)*pv_strike

    def ATFrc(self):
        # computes the reversal/conversion at the forward price
        return (self.forward - self.K)/self.interest

    def pcp(self):
        # returns the value of the put based on put-call-parity
        return self.C + (self.K - self.S) - self.rc