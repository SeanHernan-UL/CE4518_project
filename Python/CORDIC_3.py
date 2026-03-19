## CE4518 Project Work: CORDIC
## Group members (ID):  Kanvar Murray (22374698),
##                      Seán Hernan (22348948)

import math
import numpy as np
from numpy.ma.core import reshape

###
# Fails as the delta update from previous scripts no longer holds
# On each iteration a specific delta value needs to be calculated
# (we can precalculate for verilog), such that the
# tan(delta) = 2^(-i) relationship holds, i.e.
# delta = tan^(-1)(2^(-i)) for each value of i...
###

GA = math.pi/3
A = 0
steps = 18

CS = np.array([1, 0])
CS = np.reshape(CS,(2,1))

for i in range(steps):
    print(f'## Step {i} ##')

    CS_old = CS
    Delta = math.atan(2**(-i))

    if A <= GA:
        A += Delta
        CS_Delta = (1/math.sqrt(1+2**(-2*i)))*np.array([[1, -2**(-i)], [2**(-i), 1]])
        CS = np.dot(CS_Delta,CS_old)
    else:
        A -= Delta
        CS_Delta = (1/math.sqrt(1+2**(-2*i))) * np.array([[1, 2**(-i)], [-2**(-i), 1]])
        CS = np.dot(CS_Delta,CS_old)

    printAcc = 5

    print(f'C: {round(CS[0][0], printAcc)}\t\t({round(math.degrees(CS[0][0]), printAcc)})')
    print(f'S: {round(CS[1][0], printAcc)}\t\t({round(math.degrees(CS[1][0]), printAcc)})')

    print(f'D: {round(Delta, printAcc)}\t\t({round(math.degrees(Delta), printAcc)})')
    print(f'A: {round(A, printAcc)}\t\t({round(math.degrees(A), printAcc)})')

    print('')