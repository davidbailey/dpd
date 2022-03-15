form math import exp


class GravityModel:
    def __init__(self, G=1, a=1, b=1, d=1, function="inverse"):
        self.G = G
        self.a = a
        self.b = b
        self.d = d
        self.function = function

    def compute(self, mass_a=1, mass_b=1, distance=1):
        if function=="inverse":
            return self.G * (mass_a**self.a * mass_b**self.b) / distance**self.d
        elif function=="exponential":
            return self.G * (mass_a**self.a * mass_b**self.b) * exp(-self.d * distance)

