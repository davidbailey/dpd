from uuid import uuid4

from mesa import Agent


class PersonAgent(Agent):
    """
    A person
    """

    def __init__(self, model, unique_id=uuid4()):
        super().__init__(unique_id, model)
