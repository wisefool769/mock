# option_board.py
# Author: Christian Drappi
# This file contains the class for an option board
from option import Option
import calc
import math

class OptionBoard:
	def __init__(self, spot, vol, rate, time_to_exp, strike_increments = 5, n = 5):
		self.S = spot
		self.sigma = vol
		self.r = rate
		self.tau = time_to_exp
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

	def print_board(self):
		print("\nSpot: " + str(self.S) + "    r/c = " + str(self.rc))
		print(" Call\t\t Put")
		for opt in self.options:
			opt.print_option()


