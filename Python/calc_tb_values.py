
import math
import numpy as np
from calc_fixed_point import calc_fixed_point

steps = 18
test_values = np.linspace(-math.pi / 2, math.pi / 2, 1000)
for i in range(1000):
    _,test_values_fixed_point = calc_fixed_point(round(test_values[i], 8))
    print(f"test_value[{i}] = " +test_values_fixed_point+f'; // {round(test_values[i], 8)} rad')