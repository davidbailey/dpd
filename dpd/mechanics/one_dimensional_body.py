from astropy import units
from mesa import Agent
from uuid import uuid4

class OneDimensionalBody(Agent):
    """
    """

    def __init__(self, model, unique_id=None, initial_position=None):
        self.unique_id = unique_id if unique_id else uuid4()
        super().__init__(self.unique_id, model)
        self.position = initial_position if initial_position else 0 * units.meter
