from mesa import Agent

class PersonAgent(Agent):
    """
    A person
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
