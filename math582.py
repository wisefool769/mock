# math582.py

from option import Option
from numpy import cumsum, array, diff
from math import exp
import csv


num_options = 1000
round_lot = 100
year_length = 365.0

S = 54.17
K = 49.0
sigma = 0.20
r = 0.05
days_to_exp = 0.0
tau = days_to_exp/year_length



opt = Option(S, K, sigma, r, tau)
print(opt.C)
print(opt.call_delta)

# day = [0, 1, 138, 139, 140]
# day_diff = [x - day[i - 1] for i, x in enumerate(day) if i > 0]
# spot = [60.0, 60.12, 56.12, 55.86, 55.64]
# options = [Option(s, K, sigma, r, tau-(day[i]/365)) for i,s in enumerate(spot)]
# deltas = [o.call_delta for o in options]
# temp_deltas = [(10**5) * d for d in deltas]
# temp_deltas_2 = list([0] + temp_deltas[:-1])
# change_position = [temp_deltas[i] - td2 for i,td2 in enumerate(temp_deltas_2)]
# buy_sell_amt = [cp * spot[i] for i,cp in enumerate(change_position)]
# amt_owed = [buy_sell_amt[0]]
# for i,b in enumerate(buy_sell_amt[1:]):
#     amt_owed.append(b + amt_owed[i] * exp(r * day_diff[i]/year_length))

# with open("delta_hedging.csv", "w+") as f:
#     writer = csv.writer(f)
#     header = ["time (start of week)", "S(t)", "Delta(t)", "Change in Position", "Cash flow", "Amt owed with interest"]
#     writer.writerow(header)
#     for i in range(len(day)):
#         writer.writerow([day[i], spot[i], deltas[i], change_position[i], buy_sell_amt[i], amt_owed[i]])




