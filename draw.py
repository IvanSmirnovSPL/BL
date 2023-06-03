import matplotlib.pyplot as plt
import numpy as np

T = 0.2

one = np.load('201_81.npy')
second = np.load('401_161.npy')
third = np.load('1001_401.npy')

solutions = [one, second, third]

for sol in solutions:
    tau = T / (sol.shape[0] - 1)
    plt.plot(np.linspace(0, 1, num = sol.shape[1]), sol[int(T / tau)], label=f'sol_{sol.shape[1]}')

plt.legend()
plt.show()