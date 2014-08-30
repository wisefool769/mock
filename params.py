import re

seconds_to_years = 1.0/(3600*24*365)

time_shape = 1
time_scale = 1

initial_spot = 50
stock_drift = 0.06
stock_vol = 0.30

bid_regex = r'\d*\.?\d*(\s)+bid(\s)+for(\s)+\d*'
offer_regex = r'(have|offer)(\s)+([0-9])+(\s)+(at|@)(\s)+\d*\.?\d*'
market_regex = r'\d*\.?\d*(\s)*(-|at|@)(\s)*\d*\.?\d*(\s)+\d*(\s)+(up|by|x)(\s)*\d*'



months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
months = [m.lower() for m in months]

# -1 means sell
# 1 means buy
products = {}
# key is a product name
# the order of the list is the order of products
# first item in tuple is amount
# second item is call/put
products_list_spaces = ["call", "put", "combo", "straddle", 
                "strangle", "fly", "box", "reversal", "conversion",
                "iron fly", "roll", "split roll", "call spread", "put spread",
                "call calendar", "put calendar", "straddle swap"]
products_list = [e.replace(" ", "") for e in products_list_spaces]
# sort from longest to shortest in order to avoid
# situations like matching "call spread" to "call"
products_list.sort(key = lambda x: -len(x))


products["risk reversal"] = [(1,"P"), (-1,"C")]
products["combo"] = [(1, "C"), (-1, "P")]
products["straddle"] = [(1, "C"), (-1, "P")]
products["strangle"] = [(1, "P"), (-1, "C")]