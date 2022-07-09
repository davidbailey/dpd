from astropy import units
from mesa import Agent
from uuid import uuid4

class Body(Agent):
    """
    """

    def __init__(self, initial_position, model, unique_id=None):
        self.unique_id = unique_id if unique_id else uuid4()
        super().__init__(self.unique_id, model)
        self.position = initial_position
