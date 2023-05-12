from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation


class TransportationModel(Model):
    def __init__(self, agent_reporters=None, time_unit=1):
        self.datacollector = DataCollector(
            agent_reporters=agent_reporters,
            model_reporters={"time": lambda m: m.schedule.time * m.time_unit}
        )
        self.time_unit = time_unit
        self.schedule = RandomActivation(self)

    def step(self):
        self.schedule.step()

    def run(self):
        self.datacollector.collect(self)
        while self.schedule.agents:
            self.step()
            self.datacollector.collect(self)

     def get_dataframe(self):
        mvdf = self.datacollector.get_model_vars_dataframe()
        mvdf.index.set_names("Step", inplace=True)
        avdf = model.datacollector.get_agent_vars_dataframe()
        return avdf.merge(mvdf, left_index=True, right_index=True)
