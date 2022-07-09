from mesa import Agent

class Body(Agent):
    """
    A n-dimensional body.
    """

    def __init__(self, initial_position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = initial_position
        
