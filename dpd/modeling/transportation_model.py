from mesa import Model
from mesa.time import RandomActivation


class TransportationModel(Model):
    def __init__(self):
        self.schedule = RandomActivation(self)

    def step(self):
        self.schedule.step()
