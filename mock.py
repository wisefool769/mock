from option_board import OptionBoard

# TODO: 
# give information (cust offers, b/w, straddles, etc.)
# write csv file for board export

S = 51.34
sigma = .5
r = .05
month = "Jul"
k_inc = 5
num_options = 5

board = OptionBoard(S, sigma, r, month)

print(board.tau)
print(board.exp_date)