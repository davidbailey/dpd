from mesa import Model
from mesa.time import RandomActivation

BODY_AGENT_REPORTERS = {"position": "position"}
KINEMATIC_BODY_AGENT_REPORTERS = BODY_AGENT_REPORTERS | {"velocity": "velocity"}
KINEMATIC_BODY_WITH_ACCELERATION_AGENT_REPORTERS = KINEMATIC_BODY_AGENT_REPORTERS | {
    "acceleration": "acceleration"
}
DYNAMIC_BODY_AGENT_REPORTERS = KINEMATIC_BODY_WITH_ACCELERATION_AGENT_REPORTERS | {}

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
