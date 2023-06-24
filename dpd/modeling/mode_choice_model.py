from numpy.random import choice
from pandas import Series


class ModeChoiceModel:
    def __init__(self, modes, probabilities):
        self.modes = modes
        self.probabilities = probabilities

    def predict(self, people):
        data = []
        for i in range(len(people)):
            data.append(choice(self.modes, p=self.self.probabilities))
        return Series(data, index=people.index)
