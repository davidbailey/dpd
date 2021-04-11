class ModeChoiceModel:
    def __init__(self, modes=[]):
        self.modes = modes

    def predict(self):
        return self.modes[0]
