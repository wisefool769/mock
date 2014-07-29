import pricing
from option_board import OptionBoard

# TODO: 
# give information (cust offers, b/w, straddles, etc.)
# write .tex file for board export

start_day = "2014-01-01"
month_1 = "Aug"
month_2 = "Sep"
num_options = 5
num_symbols = 0
r = 0.05
num_hints = 5

symbol_params = pricing.get_tickers(num_symbols, start_day)

all_tex = ""

tex_header = "\\documentclass[]{article}\n\n\\usepackage{fullpage}\n\\pagenumbering{gobble}\n\n\\begin{document}"

tex_mid = "\n\n\\vspace{20mm}"

tex_page = "\n\n\\newpage"

tex_footer = "\n\n\\end{document}"

all_tex += tex_header

# for symbol in symbol_params:
#     S = symbol_params[symbol]["spot"]
#     sigma = symbol_params[symbol]["volatility"]
#     k_inc = symbol_params[symbol]["strike_increments"]
#     board_1 = OptionBoard(S, sigma, r, month_1, symbol, k_inc, num_options, num_hints)
#     tex_1 = board_1.to_tex()
#     board_2 = OptionBoard(S, sigma, r, month_2, symbol, k_inc, num_options, num_hints)
#     tex_2 = board_2.to_tex()
    # all_tex += tex_1 + tex_mid + tex_2 + tex_page

all_tex += tex_mid + tex_page


all_tex += tex_footer
with open("board.tex", "w+") as f:
    f.write(all_tex)




    