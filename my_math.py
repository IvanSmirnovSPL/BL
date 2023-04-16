from support_functions import FiltrationFunction
from params import PhysicsParams
from numpy.typing import NDArray
import numpy as np


class A:
    def __init__(self, parametres: PhysicsParams):
        self.f = FiltrationFunction(parametres)

    def plus_half(self, s: NDArray, i: int):
        if np.isclose(s[i + 1], s[i]):
            return self.f(s[i])
        else:
            return (self.f(s[i + 1]) - self.f(s[i])) / (s[i + 1] - s[i])

    def minus_half(self, s: NDArray, i: int):
        if np.isclose(s[i], s[i - 1]):
            return self.f(s[i - 1])
        else:
            return (self.f(s[i]) - self.f(s[i - 1])) / (s[i] - s[i - 1])


class Flow:
    def __init__(self, parametres: PhysicsParams):
        self.a = A(parametres)
        self.f = FiltrationFunction(parametres)

    def plus_half(self, s: NDArray, i: int):
        if self.a.plus_half(s, i) >= 0:
            return self.f(s[i])
        else:
            return self.f(s[i + 1])

    def minus_half(self, s: NDArray, i: int):
        if self.a.minus_half(s, i) >= 0:
            return self.f(s[i - 1])
        else:
            return self.f(s[i])


def minmod(theta: float):
    if theta <= 0:
        return 0
    elif 1 >= theta > 0:
        return theta
    else:
        return 1
