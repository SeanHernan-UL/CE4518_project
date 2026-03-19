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
    A = 0

    K = 1
    for i in range(steps):
        K *= (1 / math.sqrt(1 + 2 ** (-2 * i)))
    print(f'K: {round(K, printAcc)}\t\t({round(math.degrees(K), printAcc)})\t[{calc_fixed_point(round(K, printAcc))}])')

    # initialising CS matrix
    if GA >= 0:
        CS = np.array([K, K]).reshape([2,1])
    else:
        CS = np.array([K, -K]).reshape([2,1])

    for i in range(1, steps):
        # store old values
        CS_old = CS
        Delta = math.atan(2 ** (-i))

        # perform update
        if A <= GA:
            A += Delta
            CS_Delta = np.array([[1, -2 ** (-i)], [2 ** (-i), 1]])
            CS = np.dot(CS_Delta, CS_old)
        else:
            A -= Delta
            CS_Delta = np.array([[1, 2 ** (-i)], [-2 ** (-i), 1]])
            CS = np.dot(CS_Delta, CS_old)

        # print if enabled...
        if print_en:

            print(f'## Step {i} ##')

            print(f'C: {round(CS[0][0], printAcc)}\t\t({round(math.degrees(CS[0][0]), printAcc)})\t[{calc_fixed_point(round(CS[0][0], printAcc))}]')
            print(f'S: {round(CS[1][0], printAcc)}\t\t({round(math.degrees(CS[1][0]), printAcc)})\t[{calc_fixed_point(round(CS[1][0], printAcc))}]')

            print(f'D: {round(Delta, printAcc)}\t\t({round(math.degrees(Delta), printAcc)})\t[{calc_fixed_point(Delta)}]')
            print(f'A: {round(A, printAcc)}\t\t({round(math.degrees(A), printAcc)})\t[{calc_fixed_point(round(A, printAcc))}])')

            print('')
            print([CS[0][0], CS[1][0]])
            print('')

        if plot_en:
            plt.plot([0, CS[0][0]], [0, CS[1][0]], '-*')

    return [A, CS[0][0], CS[1][0]]


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

# for GA in np.linspace(-math.pi / 2, math.pi / 2, 1000):
#     # for GA in [-math.pi/2]:
#     for step in range(0, 100):
#         # for step in [23]:
#         prev = results
#         results = cordic(GA, step)
#         # results = cordic(GA, step, print_en=True, plot_en=True)
#
#         if (abs(results[1] - prev[1]) < LSB):
#             # print(f'SUFFICIENT ACCURACY (COS)')
#             cos_flag = 1
#
#         if (abs(results[2] - prev[2]) < LSB):
#             # print(f'SUFFICIENT ACCURACY (SIN)')
#             sin_flag = 1
#
#         if cos_flag and sin_flag:
#             print(f'GA: {GA}, STEP: {step}')
#             print(f'A: {results[0]}, C: {float(results[1]):.10f}, S: {float(results[2]):.10f}')
#             print(
#                 f'C_error: {abs(results[1] - prev[1]):.10f}, S_error: {abs(results[2] - prev[2]):.10f}, 1LSB: {LSB:.10f}')
#             print('')
#
#             num_steps.append(step)
#             # print(num_steps)
#
#             cos_flag = 0
#             sin_flag = 0
#             break
#
# # plt.grid()
# # plt.show()
#
# print('\n\n')
# print(num_steps)
# print(f'len(num_steps: {len(num_steps)}')

print(cordic(math.pi/3, 17,True))

