import math
import numpy as np
import matplotlib.pyplot as plt

python = np.loadtxt("python.txt", delimiter=',', converters=(lambda s: int(s, 16)), dtype=float)
verilog = np.loadtxt("verilog.txt", delimiter=',', converters=(lambda s: int(s, 16)), dtype=float)

error = (python - verilog)*(2**-16)

np.savetxt("error.txt", error)

# plt.plot(python[:, 1])
# plt.plot(verilog[:, 1])
fig, [ax1, ax2, ax3] = plt.subplots(3,1, figsize=(8, 7), dpi=200)
fig.suptitle('Error')

ax1.grid(True)
ax1.stem(np.linspace(-math.pi / 2, math.pi / 2, 1000)[1:-1],error[1:-1, 1], linefmt='b-',markerfmt='b.', basefmt='k')
ax1.legend(['cos'])
ax1.set_ylim([0.0002, -.0002])

ax2.grid(True)
ax2.stem(np.linspace(-math.pi / 2, math.pi / 2, 1000)[1:-1],error[1:-1, 2],  linefmt='y-',markerfmt='y.', basefmt='k')
ax2.legend(['sin'])
ax2.set_ylim([0.0002, -.0002])
ax2.set_ylabel('Error (V vs P)')

ax3.grid(True)
ax3.stem(np.linspace(-math.pi / 2, math.pi / 2, 1000)[1:-1],error[1:-1, 3], linefmt='g-', markerfmt='g.', basefmt='k')
ax3.legend(['angle'])
ax3.set_ylim([0.0002, -.0002])
ax3.set_xlabel('Angle (rad)')

plt.show()