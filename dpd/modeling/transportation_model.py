from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation


class TransportationModel(Model):
    def __init__(self, datacollector=None, time_unit=1):
        if datacollector is not None:
            self.datacollector = datacollector
        else:
            pass
        self.time_unit = time_unit
        self.schedule = RandomActivation(self)

    def step(self):
        self.schedule.step()

    def run(self):
        self.datacollector.collect(self)
        while self.schedule.agents:
            self.step()
            self.datacollector.collect(self)
