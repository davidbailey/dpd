from numpy.random import choice

class ModeChoiceModel:
    def __init__(self, modes=[], probabilities=[]):
        self.modes = modes
        self.probabilities = probabilities

    def add_mode(self, mode, probability):
        self.modes.append(mode)
        self.probabilities.append(probability)

    def predict(self):
        return choice(self.modes, p=self.probailities)
