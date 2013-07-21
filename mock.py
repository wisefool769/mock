from option_board import OptionBoard

S = 51.34
sigma = .5
r = .05
tau = 30/365
k_inc = 5
num_options = 5

board = OptionBoard(S, sigma, r, tau)

board.print_board()