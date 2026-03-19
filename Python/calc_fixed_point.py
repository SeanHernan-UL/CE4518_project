## CE4518 Project Work: CORDIC
## Group members (ID):  Kanvar Murray (22374698),
##                      Seán Hernan (22348948)

import math
import numpy as np

def calc_fixed_point(num):
    ## given a floating point number calculate the 2.16 fixed point representation of it...

    if (num >=0):
        num = math.floor(num * 2** 16) # hardware won't give us nice rounding for free, so floor time
    else: # handle two's complement
        num = ((math.floor(abs(num) * 2** 16)^0x3ffff) + 1) & 0x3ffff

    return f"{format(num, '05x')}", f"18'b{format(num, '018b')}"

# print(calc_fixed_point(0.123456))
# print(calc_fixed_point(-0.123456))

