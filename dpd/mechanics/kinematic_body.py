from .body import Body

class KinematicBody(Body):
    """
    A class to simulate a kinematic body. Provides methods to move the body with constant velocity.
    """

    def __init__(self, velocity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = velocity

    def step_position(self):
        self.position = self.position + self.velocity

    def step(self):
        self.step_position()
