import math
import numpy as np
from numpy.ma.core import reshape

def cordic(GA, steps, print_en=False):
    # init values
    A = 0
    CS = np.array([1, 0])
    CS = np.reshape(CS,(2,1))

    K = 1
    for i in range(steps):
        K*=(1/math.sqrt(1+2**(-2*i)))
    print(f'K: {K:.16f}')


    for i in range(steps):
        # store old values
        CS_old = CS
        Delta = math.atan(2**(-i))

        # perform update
        if A <= GA:
            A += Delta
            CS_Delta = K*np.array([[1, -2**(-i)], [2**(-i), 1]])
            CS = np.dot(CS_Delta,CS_old)
        else:
            A -= Delta
            CS_Delta = K * np.array([[1, 2**(-i)], [-2**(-i), 1]])
            CS = np.dot(CS_Delta,CS_old)

        # print if enabled...
        if print_en:
            printAcc = 5
            print(f'## Step {i} ##')

            print(f'C: {round(CS[0][0], printAcc)}\t\t({round(math.degrees(CS[0][0]), printAcc)})')
            print(f'S: {round(CS[1][0], printAcc)}\t\t({round(math.degrees(CS[1][0]), printAcc)})')

            print(f'D: {round(Delta, printAcc)}\t\t({round(math.degrees(Delta), printAcc)})')
            print(f'A: {round(A, printAcc)}\t\t({round(math.degrees(A), printAcc)})')

            print('')

    return [A, CS[0][0], CS[1][0]]


## 'main'

print(cordic(math.pi/3, 23))

# work out how many decimal places 16 bits of precision is...
LSB = 2**(-16)
print((f"1LSB: {LSB:.10f}"))

# do big loop
results = [-99,-99,-99]
prev = [-99,-99,-99]
cos_flag = 0
sin_flag = 0
num_steps = []
if False:
    for GA in np.linspace(-math.pi/2, math.pi/2, 1000):
        for step in range(0, 100):
            prev = results
            results = cordic(GA, step)

            if (abs(results[1] - prev[1]) < LSB):
                # print(f'SUFFICIENT ACCURACY (COS)')
                cos_flag = 1


            if (abs(results[2] - prev[2]) < LSB):
                # print(f'SUFFICIENT ACCURACY (SIN)')
                sin_flag = 1

            if cos_flag and sin_flag:
                print(f'GA: {GA}, STEP: {step}')
                print(f'A: {results[0]}, C: {float(results[1]):.10f}, S: {float(results[2]):.10f}')
                print(f'C_error: {abs(results[1] - prev[1]):.10f}, S_error: {abs(results[2] - prev[2]):.10f}, 1LSB: {LSB:.10f}')
                print('')

                num_steps.append(step)
                # print(num_steps)

                cos_flag = 0
                sin_flag = 0
                break

print('\n\n')
print(num_steps)
print(f'len(num_steps: {len(num_steps)}')

