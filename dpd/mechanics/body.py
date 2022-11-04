from mesa import Agent


class Body(Agent):
    """
    A body.
    """

    def __init__(self, initial_position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_position = initial_position
        self.position = initial_position

    def step(self):
        super().step()
