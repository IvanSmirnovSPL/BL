from my_math import Flow
import numpy as np
from params import PhysicsParams
import matplotlib.pyplot as plt

flow = Flow(PhysicsParams())

T = 1
X = 1

NT = 201
NX = 201

solution = np.zeros((NT, NX))
tau = T / (NT - 1)
h = X / (NX - 1)

for i in range(solution.shape[1]):
    solution[0][i] = 0

for n in range(solution.shape[0]):
    solution[n][0] = 1
    solution[n][-1] = 0

for n in range(solution.shape[0] - 1):
    for i in range(1, solution.shape[1] - 1):
        support = flow.minus_half(solution[n], i) - flow.plus_half(solution[n], i)
        solution[n + 1][i] = solution[n][i] - (tau / h) * (
                flow.plus_half(solution[n], i) - flow.minus_half(solution[n], i)
        )

for n in range(0, solution.shape[0], 5):
    plt.title(f'{tau * n}')
    plt.plot(solution[n], '-o')
    plt.grid()
    plt.show()

