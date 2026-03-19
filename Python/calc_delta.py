
import math
from calc_fixed_point import calc_fixed_point

steps = 18
for i in range(1, steps):
    delta = math.atan(2 ** (-i))
    delta_fixed_point,_ = calc_fixed_point(round(delta, 8))
    print(f"Delta[{i}] = 18'b"+delta_fixed_point+f'; // {round(delta, 8)} rad')