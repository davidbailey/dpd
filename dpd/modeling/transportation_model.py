from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import BaseScheduler


class TransportationModel(Model):
    def __init__(self, agent_reporters=None, time_unit=1):
        super().__init__()
        self.datacollector = DataCollector(
            agent_reporters=agent_reporters,
            model_reporters={"time": lambda m: m.schedule.time * m.time_unit},
        )
        self.time_unit = time_unit
        self.schedule = BaseScheduler(self)

    def step(self):
        if not self.schedule.agents:
            self.running = False
        self.datacollector.collect(self)
        self.schedule.step()

    def get_dataframe(self):
        mvdf = self.datacollector.get_model_vars_dataframe()
        mvdf.index.set_names("Step", inplace=True)
        avdf = self.datacollector.get_agent_vars_dataframe()
        return avdf.merge(mvdf, left_index=True, right_index=True)
