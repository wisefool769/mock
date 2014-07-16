import math
from datetime import date
# Some helper functions

def sgn(x):
    # Returns the sign of x: -1, 0, or 1
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1

def time_to_exp(month):
    delta = expiration(month) - date.today()
    return delta.days/365.0

def expiration(month):
    todays_date = date.today()
    try_year = todays_date.year
    while True:
        try_third_friday = get_third_friday(month, try_year)
        try_exp = date(try_year, month, try_third_friday)
        if try_exp > todays_date:
            break
        else:
            try_year = try_year + 1
    return try_exp

def get_third_friday(mo, yr):
    first_of_month = date(yr, mo, 1)
    day_of_week = first_of_month.weekday()
    return ((4-day_of_week) % 7) + 15

def month_to_int(month_str):
    if month_str == "Jan":
        return 1
    elif month_str == "Feb":
        return 2
    elif month_str == "Mar":
        return 3
    elif month_str == "Apr":
        return 4
    elif month_str == "May":
        return 5
    elif month_str == "Jun":
        return 6
    elif month_str == "Jul":
        return 7
    elif month_str == "Aug":
        return 8
    elif month_str == "Sep":
        return 9
    elif month_str == "Oct":
        return 10
    elif month_str == "Nov":
        return 11
    elif month_str == "Dec":
        return 12

def int_to_month(month_int):
    months = ["Jan","Feb","Mar","Apr",
                "May","Jun","Jul","Aug",
                "Sep","Oct","Nov","Dec"]
    return months[month_int-1]
