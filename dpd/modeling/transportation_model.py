from astropy import units
from mesa import Model
from mesa.time import RandomActivation


class TransportationModel(Model):
    def __init__(self, time_unit):
        self.schedule = RandomActivation(self)
        self.time_unit = time_unit

    def step(self):
        self.schedule.step()

    def run(self):
        while self.schedule.agents:
            self.step()
