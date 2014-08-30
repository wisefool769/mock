# option.py
# Author: Christian Drappi
# This file contains the class to initialize 
# an option, given certain Black-Scholes parameters

import math
import random
from calc import price_format
from scipy.stats import norm

class Option:
    def __init__(self, spot, strike, vol, rate, time_to_exp):
        # note that time to expiration here is in years,
        # as it is in the BSM model.
        self.S = spot
        self.K = strike
        self.sigma = vol
        self.r = rate
        self.tau = max(time_to_exp,0)
        self.forward = self.S*math.exp(self.r*self.tau)
        self.rc = self.get_ATFrc()
        self.vol_adj_time = self.sigma * math.sqrt(self.tau)
        self.d1 = 1/self.vol_adj_time*(math.log(self.S/self.K) + (self.r + 0.5 * self.sigma ** 2) * self.tau)
        self.d2 = self.d1 - self.vol_adj_time
        self.C = self.bsm_call()
        self.P = self.pcp_put()
        # self.call_delta = self.get_call_delta()
        # self.put_delta = self.call_delta - 1.0
        # self.call_vega = self.get_call_vega()
        # self.put_vega = self.call_vega
        # self.call_theta = self.get_call_theta()
        # self.put_theta = self.call_theta
        # self.call_gamma = self.get_call_gamma()
        # self.put_gamma = self.get_put_gamma()

    def bsm_call(self):
        # returns the Black-Scholes Merton value of
        # the call from option's parameters
        if self.tau == 0:
            return max(self.S-self.K, 0)
        else:
            pv_strike = self.K*math.exp(-1*self.r*self.tau)
            call_price = norm.cdf(self.d1)*self.S - norm.cdf(self.d2)*pv_strike
            return self.smooth_call(call_price)

    def smooth_call(self, call_price):
        # the constant r/c gives these values an error from 
        # bsm prices, and so we evenly express this error in 
        # the call (by adding rc/2) and the put (subtracting rc)
        # pv_interest = self.K - self.K*math.exp(-1*self.r*self.tau)
        # call = max(bsm_call+(self.rc-pv_interest)/2, 0)
        call = max(call_price, 0)
        return round(call, 2)

    def get_ATFrc(self):
        # computes the reversal/conversion at the forward price
        rc = self.forward*(1-math.exp(-1*self.r*self.tau))
        return round(20*rc)/20.0

    # def get_rate(self):
    #     # computes the rate r given an r/c
    #     return 1/self.tau*math.log(1.0+self.rc/self.S)

    def pcp_put(self):
        # returns the value of the put based on put-call-parity
        put = max(self.C + (self.K - self.S) - self.rc,0)
        return round(put,2)

    def get_call_delta(self):
        if self.tau == 0:
            return 1 if self.S > self.K else 0
        else:
            return norm.cdf(self.d1)

    def get_call_vega(self):
        return None

    def get_call_theta(self):
        return None

    def get_call_gamma(self):
        return None
            
    def print_option(self):
        print(price_format(self.C) + "\t" + str(self.K) + "\t" + price_format(self.P))
