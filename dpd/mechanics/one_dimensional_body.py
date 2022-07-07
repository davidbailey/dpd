from astropy import units
from mesa import Agent
from uuid import uuid4

class OneDimensionalBody(Agent):
    """
    """

    def __init__(self, model):
        self.unique_id = uuid4()
        super().__init__(self.unique_id, model)
        self.position = 0 * units.meter
