# option_board.py
# Author: Christian Drappi
# This file contains the class for an option board
from option import Option
import calc
import math

class OptionBoard:
	def __init__(self, spot, vol, rate, exp_mo, strike_increments = 5, n = 5):
		self.S = spot
		self.sigma = vol
		self.r = rate
		self.exp_month = self.exp_month_str(exp_mo)
		self.exp_month_num = self.exp_month_int(exp_mo)
		self.tau = calc.time_to_exp(self.exp_month_num)
		self.exp_date = calc.expiration(self.exp_month_num)
		self.k_inc = strike_increments
		self.num_options = n
		self.strikes = self.get_strikes()
		self.options = self.get_options(self.strikes)
		self.rc = self.options[0].rc
		
	def get_strikes(self):
		nearest_increment = round(self.S / self.k_inc) * self.k_inc
		direction = calc.sgn(self.S-self.k_inc)
		begin = -1*math.floor(self.num_options/2)
		strikes = []
		if (self.num_options % 2 == 0) and (direction == 1):
		# Strange edge case: if we want an even number of options
		# and our spot is higher than our first increment,
		# then the extra option we include will be higher.
			begin += 1
		for i in range(self.num_options):
			k = nearest_increment + (begin+i)*self.k_inc
			strikes.append(k)
		return strikes

	def get_options(self, strikes):
		options = []
		for k in strikes:
			options.append(Option(self.S, k, self.sigma, self.r, self.tau))
		return options

	def exp_month_int(self, exp_mo):
		if isinstance(exp_mo, int):
			return exp_mo
		else:
			return calc.month_to_int(exp_mo)

	def exp_month_str(self, exp_mo):
		if isinstance(exp_mo, int):
			return calc.int_to_month(exp_mo)
		else:
			return exp_mo

	def print_board(self):
		print("\nSpot: " + str(self.S) + "    r/c = " + str(self.rc))
		print(" Call\t"+self.exp_month+"\t Put")
		for opt in self.options:
			opt.print_option()


