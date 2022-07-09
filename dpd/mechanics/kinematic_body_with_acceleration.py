import numpy

from .kinematic_body import KinematicBody


class KinematicBodyWithAcceleration(KinematicBody):
    """
    A class to simulate a kinematic body. Provides methods to move the body with constant acceleration and decelerate the body with constant deceleration.
    """

    def __init__(self, initial_acceleration, max_velocity=None, min_velocity=None, max_deceleration=None, final_velocity=None, *args, **kwargs):
        self.acceleration = initial_acceleration
        self.max_velocity = max_velocity
        self.min_velocity = min_velocity
        self.max_deceleration = max_deceleration
        self.final_velocity = final_velocity
        super().__init__(*args, **kwargs)

    def step_velocity(self):
        self.velocity = self.velocity + self.acceleration
        if self.max_velocity:
            self.velocity = numpy.maximum(self.velocity, self.max_velocity)
        if self.min_velocity:
            self.velocity = numpy.minimum(self.velocity, self.min_velocity)
        if self.max_deceleration and self.final_velocity:
            stopping_distance_velocity_max_position = numpy.sqrt(self.final_velocity**2 + 2 * self.max_deceleration * (self.max_position - self.position))
            self.velocity = numpy.minimum(self.velocity, stopping_distance_velocity_max_position)
            stopping_distance_velocity_min_position = numpy.sqrt(self.final_velocity**2 + 2 * self.max_deceleration * (self.min_position - self.position))
            self.velocity = numpy.minimum(self.velocity, stopping_distance_velocity_min_position)
            self.acceleration = self.max_deceleration
            
    def step(self):
        self.step_velocity()
        super().step()
        
