from mesa import Model
from mesa.time import RandomActivation


class TransportationModel(Model):
    def __init__(self, datacollector=None, time_unit=1):
        self.datacollector = datacollector
        self.time_unit = time_unit
        self.schedule = RandomActivation(self)

    def step(self):
        self.schedule.step()

    def run(self):
        self.datacollector.collect(self)
        while self.schedule.agents:
            self.step()
            self.datacollector.collect(self)
