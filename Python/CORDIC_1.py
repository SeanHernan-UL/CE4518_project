import math
import numpy as np
from numpy.ma.core import reshape

GA = math.pi/3
Delta = math.pi/4
A = 0
steps = 10

CS = np.array([1, 0])
CS = np.reshape(CS,(2,1))

for i in range(steps):
    print(f'## Step {i} ##')

    CS_old = CS

    if A <= GA:
        A += Delta
        CS_Delta = np.array([[math.cos(Delta), -math.sin(Delta)], [math.sin(Delta), math.cos(Delta)]])
        CS = np.dot(CS_Delta,CS_old)
    else:
        A -= Delta
        CS_Delta = np.array([[math.cos(Delta), math.sin(Delta)], [-math.sin(Delta), math.cos(Delta)]])
        CS = np.dot(CS_Delta,CS_old)


    printAcc = 5

    print(f'C: {round(CS[0][0], printAcc)}\t\t({round(math.degrees(CS[0][0]), printAcc)})')
    print(f'S: {round(CS[1][0], printAcc)}\t\t({round(math.degrees(CS[1][0]), printAcc)})')

    print(f'D: {round(Delta, printAcc)}\t\t({round(math.degrees(Delta), printAcc)})')
    print(f'A: {round(A, printAcc)}\t\t({round(math.degrees(A), printAcc)})')

    Delta = Delta / 2

    print('')