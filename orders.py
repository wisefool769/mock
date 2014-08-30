# this script accepts orders from the python terminal
# written in english and encodes them for processing
import params as p
import re
from calc import isfloat, contains_substring, which_substring

class Order:
    def __init__(self, prices, quantities, direction, product, months, strikes):
        self.prices = prices
        self.quantities = quantities
        self.direction = direction
        self.product = product
        self.months = months
        self.strikes = strikes

    def to_string(self):
        ret = "{'prices': " + str(self.prices) + ", "
        ret += "'quantities': " + str(self.quantities) + ", "
        ret += "'direction': " + str(self.direction) + ", "
        ret += "'product': " + str(self.product) + ", "
        ret += "'months': " + str(self.months) + ", "
        ret += "'strikes': " + str(self.strikes) + "}"
        return ret


def get_direction(order):
    if re.search(p.market_regex, order):
        direction = "market"
    elif re.search(p.bid_regex, order):
        direction = "bid"  
    elif re.search(p.offer_regex, order):
        direction = "offer"
    else:
        return False
    return direction

def get_prices_and_quantities(order_desc, direction):
    first_number_index = [1 if isfloat(e) else 0 for e in order_desc].index(1)
    info = order_desc[first_number_index:]
    if direction == "bid":
        prices = [float(info[0])]
        quantities = [int(info[3])]
    elif direction == "offer":
        prices = [float(info[2])]
        quantities = [int(info[0])]
    elif direction == "market":
        prices = [float(info[0]), float(info[2])]
        quantities = [int(info[3])]
        if "up" not in info:
            quantities.append(int(info[5]))
    else:
        return False, False
    return prices, quantities

def merge_products(order):
    ret = order
    for e in p.products_list_spaces:
        if " " in e:
            ret.replace(e, e.replace(" ", ""))
    return ret


def process_order(order):
    split_order = order.replace("/", " ").split(" ")
    product = which_substring(order, p.products_list)
    product_index = split_order.index(product)
    product_description = split_order[0:product_index]
    order_description = split_order[product_index+1:]
    months = [m for m in product_description if m in p.months]
    strikes = [float(k) for k in product_description if isfloat(k)]
    direction = get_direction(" ".join(order_description))
    prices, quantities = get_prices_and_quantities(order_description, direction)
    order_object = Order(prices, quantities, direction, product, months, strikes)
    if not (prices and quantities and direction and product and months and strikes):
        print("Bad order - try again")
        return False
    else:
        return order_object.to_string()

if __name__ == "__main__":
    print("\nEnter your orders below\n")
    while True:
        active_order = input("--> ").lower()
        to_write = process_order(active_order)
        if to_write:
            with open("orders.txt", "a+") as f:
                f.write(to_write+"\n")




