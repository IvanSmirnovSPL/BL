from dataclasses import dataclass

@dataclass(frozen=True)
class PhysicsParams:
    mu_water = 0.5
    mu_oil = 3.3