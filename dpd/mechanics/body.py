from mesa import Agent

class Body(Agent):
    """
    An n-dimensional body.
    """

    def __init__(self, initial_position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_position = initial_position
        self.position = initial_position
        
    def step(self):
        pass
