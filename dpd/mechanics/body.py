from astropy import units
from mesa import Agent
from uuid import uuid4

class Body(Agent):
    """
    """

    def __init__(self, initial_position, unique_id=None, *args, **kwargs):
        unique_id = unique_id if unique_id else uuid4()
        super().__init__(unique_id, *args, **kwargs)
        self.position = initial_position
