## CE4518 Project Work: CORDIC
## Group members (ID):  Kanvar Murray (22374698),
##                      Seán Hernan (22348948)

import math
import numpy as np
from numpy.ma.core import reshape
import matplotlib.pyplot as plt
from calc_fixed_point import calc_fixed_point

printAcc = 8

def cordic(GA, steps, print_en=False, plot_en=False):
    # init values

    K = 1
    for i in range(steps):
        K *= (1 / math.sqrt(1 + 2 ** (-2 * i)))
    # print(f'K: {round(K, printAcc)}\t\t({round(math.degrees(K), printAcc)})\t[{calc_fixed_point(round(K, printAcc))}])')

    # initialising CS matrix
    if GA >= 0:
        A = math.radians(45)
        C = K
        S = K
    else:
        A = -math.radians(45)
        C = K
        S = -K

    # print(f'A: {round(A, printAcc)}\t\t({round(math.degrees(A), printAcc)})\t[{calc_fixed_point(round(A, printAcc))}])')

    for i in range(1, steps):
        # store old values
        C_old = C
        S_old = S
        Delta = math.atan(2 ** (-(i))) # lookup in verilog

        # perform update
        if A <= GA:
            A += Delta
            C = (C_old - (S_old*2**(-i)))
            S = (C_old*2**(-i) + S_old)
        else:
            A -= Delta
            C = (C_old + (S_old * 2 ** (-i)))
            S = (-C_old * 2 ** (-i) + S_old)

        # print if enabled...
        if print_en:

            print(f'## Step {i} ##')

            print(f'C: {round(C, printAcc)}\t\t\t({round(math.degrees(C), printAcc)})\t\t[{calc_fixed_point(round(C, printAcc))}]')
            print(f'S: {round(S, printAcc)}\t\t\t({round(math.degrees(S), printAcc)})\t\t[{calc_fixed_point(round(S, printAcc))}]')

            print(f'C_old: {round(C_old, printAcc)}\t\t({round(math.degrees(C_old), printAcc)})\t\t[{calc_fixed_point(round(C_old, printAcc))}]')
            print(f'S_old: {round(S_old, printAcc)}\t\t({round(math.degrees(S_old), printAcc)})\t\t[{calc_fixed_point(round(S_old, printAcc))}]')

            print(f'D: {round(Delta, printAcc)}\t\t\t({round(math.degrees(Delta), printAcc)})\t\t[{calc_fixed_point(Delta)}]')
            print(f'A: {round(A, printAcc)}\t\t\t({round(math.degrees(A), printAcc)})\t\t[{calc_fixed_point(round(A, printAcc))}])')

            print('')
            print([C, S])
            print('')

        if plot_en:
            plt.plot([0, C], [0, S], '-*')

    return [A, C, S]


## 'main'

print(cordic(math.pi / 3, 23))

# work out how many decimal places 16 bits of precision is...
LSB = 2 ** (-16)
print((f"1LSB: {LSB:.10f}"))

# do big loop
results = [-99, -99, -99]
prev = [-99, -99, -99]
cos_flag = 0
sin_flag = 0
num_steps = []

GA = np.linspace(-math.pi / 2, math.pi / 2, 1000)
for i in range(1000):
    # for GA in [-math.pi/2]:
    for step in range(0, 100):
        # for step in [23]:
        prev = results
        results = cordic(GA[i], step)
        # results = cordic(GA, step, print_en=True, plot_en=True)

        if (abs(results[1] - prev[1]) < LSB):
            # print(f'SUFFICIENT ACCURACY (COS)')
            cos_flag = 1

        if (abs(results[2] - prev[2]) < LSB):
            # print(f'SUFFICIENT ACCURACY (SIN)')
            sin_flag = 1

        if cos_flag and sin_flag:
            A,_ = calc_fixed_point(round(results[0], printAcc))
            C,_ = calc_fixed_point(round(results[1], printAcc))
            S,_ = calc_fixed_point(round(results[2], printAcc))
            print(f'{i}, {C}, {S}, {A}')

            num_steps.append(step)
            # print(num_steps)

            cos_flag = 0
            sin_flag = 0
            break
#
# # plt.grid()
# # plt.show()
#
# print('\n\n')
# print(num_steps)
# print(f'len(num_steps: {len(num_steps)}')

# print(cordic(0.12345, 17,True))

