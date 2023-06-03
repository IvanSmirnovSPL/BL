from my_math import Flow
import numpy as np
from params import PhysicsParams
from support_functions import FiltrationFunction
from scipy import optimize
from matplotlib import pyplot as plt


# b = FiltrationFunction(PhysicsParams())
#
# from matplotlib import pyplot as plt
#
# data = np.linspace(0, 1, num=1000)
# x = data
# y = [b.der(_s) for _s in data].copy()
# plt.plot(x, y)
# plt.show()
#
# max_val = 0
# s_c = 0
# for _x, _y in zip(x[1:], y[1:]):
#     if _y / _x > max_val:
#         max_val = _y / _x
#         s_c = _x
# w = b(s_c) / s_c
# print(w)
# plt.plot(data, [b(_s) for _s in data])
# plt.scatter(s_c, b(s_c))
# plt.show()


class AnalyticSolution:
    def __init__(self, params: PhysicsParams):
        self.b = FiltrationFunction(PhysicsParams())
        self.determineSc()

    def determineSc(self):
        self.s = np.linspace(0, 1, num=1000)
        max_val = 0
        self.Sc = 0
        def func(s):
            return self.b.der(s) - (self.b(s) - self.b(0)) / s
        self.Sc = optimize.root_scalar(func, bracket=[0.1, 1], method="bisect").root
        print(self.Sc)
        self.w = self.b(self.Sc) / self.Sc

    def __call__(self, t: float):
        x = np.linspace(0, 1, num=1001)
        res = np.zeros(1001)
        Xc = self.w * t
        edge = np.where(x > Xc)[0][0]
        for idx in range(0, edge):
            _x = x[idx]
            rP = _x / (t)

            def func(s):
                return self.b.der(s) - rP

            sol = optimize.root_scalar(func, bracket=[0.3, 1], method="bisect").root
            res[idx] = sol
        return (x, res)



# u = np.zeros((20000, 10001))
# u[:, 0] = 1
# for n in range(0, 19999):
#     for i in range(1, 10000):
#         u[n + 1, i] = u[n, i] - 0.1 * (b(u[n, i]) - b(u[n, i - 1]))

def vanleer(r):
    if r <= 0:
        return 0
    else:
        return 2 * r / (1 + r)

def minmod(r):
    if r <= 0:
        return 0
    if 0 < r < 1:
        return r
    if r >= 1:
        return 1


def r_p(u_i_m_1, u_i, u_i_p_1):
    if (u_i - u_i_m_1) == 0:
        return 0
    if (u_i_p_1 - u_i) == 0:
        return np.sign(u_i - u_i_m_1)
    return (u_i - u_i_m_1) / (u_i_p_1 - u_i)

def r_m(u_i_m_1, u_i, u_i_p_1):
    if (u_i_p_1 - u_i) == 0:
        return 0
    if (u_i - u_i_m_1) == 0:
        return np.sign(u_i_p_1 - u_i)
    return (u_i_p_1 - u_i) / (u_i - u_i_m_1)

b = FiltrationFunction(PhysicsParams())
def flux_HO(u_minus, u_plus):
    u_tmp = 0.5 * (u_plus + u_minus) - 0.5 * (tau / h) * (b(u_plus) - b(u_minus))
    return b(u_tmp)

def flux_LO(u_minus, u_plus):
    u_tmp = 0.5 * (u_plus + u_minus)
    return 0.5 * (b(u_minus) + b(u_plus)) - 0.5 * (h / tau) * (u_plus - u_minus)

def flux_LO(u_minus, u_plus):
    return b(u_minus)
#     if u_minus > 0 and u_plus > 0:
#         return b(u_minus)
#     elif u_minus < 0 and u_plus < 0:
#         return b(u_plus)
#     elif u_minus >= 0 >= u_plus:
#         return b(u_plus) + b(u_minus)
#     else:
#         return 0



def flux_p(u_i_m_1, u_i, u_i_p_1):
    #return flux_LO(u_i, u_i_p_1)
    return flux_LO(u_i, u_i_p_1) + minmod(r_p(u_i_m_1, u_i, u_i_p_1)) * (flux_HO(u_i, u_i_p_1) - flux_LO(u_i, u_i_p_1))

def flux_m(u_i_m_1, u_i, u_i_p_1):
    #return flux_LO(u_i_m_1, u_i)
    return flux_LO(u_i_m_1, u_i) + minmod(r_m(u_i_m_1, u_i, u_i_p_1)) * (flux_HO(u_i_m_1, u_i) - flux_LO(u_i_m_1, u_i))

h = 0.2 * 1e-2
tau = 0.1 * h
T = 0.5
N = int(T / tau) + 1
M = int(1 / h) + 1
solution = np.zeros((N, M))
solution[:, 0] = 1

from tqdm import tqdm
for n in tqdm(range(N - 1)):
    for m in range(1, M - 1):
        tmp = [solution[n, m - 1], solution[n, m], solution[n, m + 1]]
        solution[n + 1, m] = solution[n, m] - (tau / h) * (flux_p(*tmp) - flux_m(*tmp))

np.save(f'{M}_{N}', solution)

a = AnalyticSolution(PhysicsParams())
from matplotlib import pyplot as plt
for i in range(5):
    t = 1e-13 + i * 0.05
    x, y = a(t)
    plt.plot(x, y, label=f'{"%.2e" % t}')
    plt.plot(np.linspace(0, 1, num=M), solution[int(t / tau)], '-o', label='numeric')
plt.legend()
plt.show()