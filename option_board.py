# option_board.py
# Author: Christian Drappi
# This file contains the class for an option board
from option import Option
import calc
import math
from numpy.random import binomial as binom
from random import sample

class OptionBoard:
	def __init__(self, spot, vol, rate, exp_mo, ticker, strike_increments = 5, n = 5, n_hints = 5):
		self.S = spot
		self.sigma = vol
		self.r = rate
		self.symbol = ticker
		self.num_hints = n_hints
		self.exp_month = self.exp_month_str(exp_mo)
		self.exp_month_num = self.exp_month_int(exp_mo)
		self.tau = calc.time_to_exp(self.exp_month_num)
		self.exp_date = calc.expiration(self.exp_month_num)
		self.k_inc = strike_increments
		self.num_options = n
		self.strikes = self.get_strikes()
		self.options = self.get_options(self.strikes)
		self.rc = self.options[0].rc
		self.hint = self.get_hints()
		
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
			k = float(nearest_increment + (begin+i)*self.k_inc)
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
		print("\\nSpot: " + str(self.S) + "    r/c = " + str(self.rc))
		print(" Call\\t"+self.exp_month+"\\t Put")
		for opt in self.options:
			opt.print_option()



	# c - p = s - k + r/c
		
	# put side
	# buy/write
	# put spread
	# put flys

	# either side
	# combo
	# straddle
	# strangle
	# collar ()
	# risk reversal (long put short call)
	# calendar
	# diagonal


	def get_hints(self):
		nh = self.num_hints
		hints = [None]*(2*self.num_options)
		hints_placement = sample([2*i for i in range(self.num_options)], nh)
		hint_side = [binom(1, 0.5) for i in range(nh)]
		hints_location = [hint_side[i]+hints_placement[i] for i in range(nh)]
		no_hint = list(set(range(2*self.num_options)) - set(hints_location))
		for n in no_hint:
			hints[n] = "\parbox[][][t]{40mm}{\hspace{40mm}}"
		for h in hints_location:
			# evens are call hints
			if h % 2 == 0:
				hints[h] = self.get_call_hint(int(h/2))
			else:
				hints[h] = self.get_put_hint(int(h/2))
		return hints

	def get_call_hint(self, loc):
		# if it's on the bottom, we can't do call spreads/flys
		if loc == 4:
			return self.get_puts_and_stock(loc)
		else:
			return self.get_puts_and_stock(loc)
		# call side
		# p+s
		# call spread
		# call flys

	def get_put_hint(self, loc):
		# if it's on the bottom, we can't do put spreads/flys
		if loc == 4:
			return self.get_buy_write(loc)
		else:
			return self.get_buy_write(loc)

	# c - p = s-k + r/c
	# c - (s-k) = p + r/c

	def get_buy_write(self, loc):
		return "\parbox[][][t]{40mm}{" + calc.price_format(self.strikes[loc]) + " b/w = " + calc.price_format(self.options[loc].P + self.rc) + "}"

	def get_puts_and_stock(self, loc):
		return "\parbox[][][t]{40mm}{" + calc.price_format(self.strikes[loc]) + " p+s = " + calc.price_format(self.options[loc].C - self.rc) + "}"


	def to_tex(self, k_inc):
		dec = k_inc == 2.50

		tex = """\\Large

		\\begin{center}{\parbox[][4.5 mm][t]{40mm}{""" + self.symbol + " \\$ " + calc.price_format(self.S) + "} \\hspace{5mm} \\textbf{" + self.exp_month + "} \\hspace{20mm} r/c = " + calc.price_format(self.rc) + """}\\end{center}

		\\vspace{5mm}

		\\begin{center} {Calls \\hspace{28mm} Strike \\hspace{26mm} Puts}\\end{center}
		\\vspace{5mm}
		\\large """ + self.hint[0] + """ \\hspace{36.5mm} \\LARGE """ + "\parbox[][][t]{10mm}{\\centering " +  calc.price_format(self.strikes[0], dec) + """} \\hspace{55mm} \\large """ + self.hint[1] + """ \\vspace{6.5mm} \\\\
		\\large """ + self.hint[2] + """ \\hspace{36.5mm} \\LARGE """ + "\parbox[][][t]{10mm}{\\centering " + calc.price_format(self.strikes[1], dec) + """} \\hspace{55mm} \\large """ + self.hint[3] + """ \\vspace{6.5mm} \\\\
		\\large """ + self.hint[4] + """ \\hspace{36.5mm} \\LARGE """ + "\parbox[][][t]{10mm}{\\centering " + calc.price_format(self.strikes[2], dec) + """} \\hspace{55mm} \\large """ + self.hint[5] + """ \\vspace{6.5mm} \\\\
		\\large """ + self.hint[6] + """ \\hspace{36.5mm} \\LARGE """ + "\parbox[][][t]{10mm}{\\centering " + calc.price_format(self.strikes[3], dec) + """} \\hspace{55mm} \\large """ + self.hint[7] + """ \\vspace{6.5mm} \\\\
		\\large """ + self.hint[8] + """ \\hspace{36.5mm} \\LARGE """ + "\parbox[][][t]{10mm}{\\centering " + calc.price_format(self.strikes[4], dec) + """} \\hspace{55mm} \\large """ + self.hint[9]
		return tex

