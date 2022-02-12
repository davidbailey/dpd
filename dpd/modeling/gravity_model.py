class GravityModel:
    def __init__(self, G=1, a=1, b=1, d=1):
        self.G = G
        self.a = a
        self.b = b
        self.d = d

    def compute(self, mass_a, mass_b, distance):
        return self.G * (mass_a**self.a * mass_b**self.b) / distance**self.d
