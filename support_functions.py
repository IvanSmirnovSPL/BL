from params import PhysicsParams
from abc import abstractmethod, ABC


class Penetration:
    @abstractmethod
    def __init__(self, parametres: PhysicsParams): ...

    @abstractmethod
    def __call__(self, s): ...


class WaterPenetration(Penetration, ABC):
    def __init__(self, parametres: PhysicsParams):
        pass

    def __call__(self, s: float):
        return s


class OilPenetration(Penetration, ABC):
    def __init__(self, parametres: PhysicsParams):
        pass

    def __call__(self, s: float):
        return 1 - s


class FiltrationFunction:
    def __init__(self, parametres: PhysicsParams):
        self.mu_water = parametres.mu_water
        self.mu_oil = parametres.mu_oil
        self.k_water = WaterPenetration(parametres)
        self.k_oil = OilPenetration(parametres)

    def __call__(self, s: float):
        return self.k_water(s) / (
                self.k_water(s) + (self.mu_water / self.mu_oil) * self.k_oil(s)
        )
