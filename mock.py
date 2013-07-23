from option_board import OptionBoard

# TODO: 
# give information (cust offers, b/w, straddles, etc.)
# write csv file for board export

S = 50
sigma = .5
r = -.25
month = 8
k_inc = 5
num_options = 5

board = OptionBoard(S, sigma, r, month)
board.print_board()