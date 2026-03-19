## CE4518 Project Work: CORDIC
## Group members (ID):  Kanvar Murray (22374698),
##                      Seán Hernan (22348948)

import math

GA = math.pi/3
Delta = math.pi/4
A = 0
steps = 17

C = 1
S = 0


for i in range(steps):
    print(f'## Step {i} ##')
    print('')
    C_old = C
    S_old = S

    if A <= GA:
        A += Delta
        C = math.cos(Delta)*C_old - math.sin(Delta)*S_old
        S = math.sin(Delta)*C_old + math.cos(Delta)*S_old
    else:
        A -= Delta
        C = math.cos(Delta) * C_old + math.sin(Delta) * S_old
        S = -math.sin(Delta) * C_old + math.cos(Delta) * S_old

    printAcc = 5

    print(f'C: {round(C, printAcc)}\t\t({round(math.degrees(C), printAcc)})')
    print(f'S: {round(S, printAcc)}\t\t({round(math.degrees(S), printAcc)})')

    print(f'D: {round(Delta, printAcc)}\t\t({round(math.degrees(Delta), printAcc)})')
    print(f'A: {round(A, printAcc)}\t\t({round(math.degrees(A), printAcc)})')

    Delta = Delta / 2

    print('\n\n')