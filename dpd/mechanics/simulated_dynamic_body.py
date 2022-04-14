from .simulated_kinematic_body_with_acceleration import (
    SimulatedKinematicBodyWithAcceleration,
)


class SimulatedDynamicBody(SimulatedKinematicBodyWithAcceleration):
    """
    A class to simulate a dynamic body. Provides methods to move the body with constant power.
    """

    def __init__(self, power, mass, acceleration_limit, *args, **kwargs):
        self.power = power
        self.mass = mass
        self.acceleration_limit = acceleration_limit
        super().__init__(*args, **kwargs)

    def step_acceleration(self, write):
        next_acceleration = self.power / (self.mass * self.current_velocity)
        next_acceleration = min(next_acceleration, self.acceleration_limit)
        if write:
            self.current_acceleration = next_acceleration
        return next_acceleration

    def step(self, write=True):
        next_time = self.step_time(write=write)
        next_distance = self.step_distance(write=write)
        return next_time, next_distance
