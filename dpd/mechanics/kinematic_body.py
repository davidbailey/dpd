import numpy

from .body import Body

class KinematicBody(Body):
    """
    A class to simulate a kinematic body. Provides methods to move the body with constant velocity.
    """

    def __init__(self, velocity, max_position=None, min_position=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = velocity
        self.max_position = max_position
        self.min_position = min_position

    def step_position(self):
        self.position = self.position + self.velocity
        if self.max_position:
            self.position = numpy.maximum(self.position, self.max_position)
        if self.min_position:
            self.position = numpy.minimum(self.position, self.min_position)

    def step(self):
        self.step_position()
