from astropy import units
from numpy import sqrt


class KinematicBody:
    """
    A class to model a kinematic body. Provides methods to move the body with constant velocity or constant acceleration.
    """

    def __init__(
        self,
        initial_time=0 * units.second,
        initial_distance=0 * units.meter,
        initial_velocity=0 * units.meter / units.second,
        initial_acceleration=0 * units.meter / units.second**2,
    ):
        self.time = initial_time
        self.distance = initial_distance
        self.velocity = initial_velocity
        self.acceleration = initial_acceleration

    def get_body(self):
        """
        Returns the current state of all attributes that describe the body.
        """
        return self.time, self.distance, self.velocity, self.acceleration

    def set_body(self, time, distance, velocity, acceleration):
        self.time += time
        self.distance += distance
        self.velocity += velocity
        self.acceleration += acceleration

    def move_with_constant_velocity(
        self, velocity=None, time=None, distance=None, set_body=False
    ):
        """
        Moves an incremental time or distance with constant velocity (acceleration is zero).
        """
        acceleration = 0 * units.meter / units.second**2
        if velocity is None:
            velocity = self.velocity
        if time is not None:
            distance = self.velocity * time
        elif distance is not None:
            time = distance / self.velocity
        if set_body:
            set_body(time, distance, velocity, acceleration)
        return time, distance, velocity, acceleration

    def move_with_constant_acceleration(
        self, acceleration=None, time=None, distance=None, velocity=None, set_body=False
    ):
        """
        Moves an incremental time, distance, or velocity with constant acceleration.
        """
        if acceleration is None:
            acceleration = self.acceleration
        if time is not None:
            distance = self.velocity * time + 0.5 * self.acceleration * time**2
            velocity = self.acceleration * time
        elif distance is not None:
            final_velocity = sqrt(self.velocity**2 + 2 * self.acceleration * distance)
            time = (final_velocity - self.velocity) / self.acceleration
            velocity = final_velocity - self.velocity
        elif velocity is not None:
            time = velocity / self.acceleration
            return self.move_with_constant_acceleration(time=time, set_body=set_body)
        if set_body:
            set_body(time, distance, velocity, acceleration)
        return time, distance, velocity, acceleration
