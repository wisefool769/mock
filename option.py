# option.py
# Author: Christian Drappi
# This file contains the class to initialize 
# an option, given certain Black-Scholes parameters

import math
import random
from scipy.stats import norm
 


class Option:
    def __init__(self, spot, strike, vol, rate, time_to_exp):
        # note that time to expiration here is in years,
        # as it is in the BSM model.
        self.S = spot
        self.K = strike
        self.sigma = vol
        self.r = rate
        self.tau = time_to_exp
        self.forward = self.S*math.exp(self.r*self.tau)
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
        call = max(norm.cdf(d1)*self.S - norm.cdf(d2)*pv_strike,0)
        return round(call,2)

    def ATFrc(self):
        # computes the reversal/conversion at the forward price
        rc = self.forward*(1-math.exp(-1*self.r*self.tau))
        return round(rc, 2)

    def pcp(self):
        # returns the value of the put based on put-call-parity
        put = max(self.C + (self.K - self.S) - self.rc,0)
        return round(put,2)

    def print_option(self):
        print(str(self.C) + "\t" + str(self.K) + "\t" + str(self.P))
