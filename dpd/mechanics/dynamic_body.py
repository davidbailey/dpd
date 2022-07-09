from .kinematic_body_with_acceleration import KinematicBodyWithAcceleration

class DynamicBody(KinematicBodyWithAcceleration):
    """
    A class to simulate a dynamic body. Provides methods to move the body with constant power.
    """

    def __init__(self, power, mass, max_acceleration=None, min_acceleration=None, *args, **kwargs):
        self.power = power
        self.mass = mass
        self.max_acceleration = max_acceleration
        self.min_acceleration = min_acceleration
        super().__init__(*args, **kwargs)

    def step_acceleration(self):
        self.acceleration = self.power / (self.mass * self.velocity)
        if self.max_acceleration:
            self.acceleration = numpy.maximum(self.acceleration, self.max_acceleration)
        if self.min_acceleration:
            self.acceleration = numpy.minimum(self.acceleration, self.min_acceleration)

    def step(self):
        self.step_acceleration()
        self.step_velocity()
        self.step_position()
        
