from astropy import units

from .simulated_kinematic_body import SimulatedKinematicBody


class SimulatedKinematicBodyWithAcceleration(SimulatedKinematicBody):
    """
    A class to simulate a kinematic body. Provides methods to move the body with constant acceleration and decelerate the body with constant deceleration.
    """

    def __init__(self, velocity_limit=None, max_deceleration, *args, **kwargs):
        self.current_acceleration = 0 * units.meter / units.second**2
        self.velocity_limit = velocity_limit
        self.max_deceleration = max_deceleration
        super().__init__(*args, **kwargs)

    def step_acceleration(self, write):
        return self.current_acceleration

    def step_velocity(self, write):
        next_velocity = (
            self.current_velocity + self.step_acceleration(write) * self.delta_time
        )
        if self.velocity_limit:
            next_velocity = min(next_velocity, self.velocity_limit)
        if write:
            self.current_velocity = next_velocity
        return next_velocity

    def step(self, write=True):
        next_time = self.step_time(write=write)
        next_distance = self.step_distance(write=write)
        return next_time, next_distance

    def stopping_distance(self, final_velocity):
        return (final_velocity**2 - self.current_velocity**2) / (
            2 * self.max_deceleration
        )

    def decelerate(self, distance, final_velocity):
        self.current_time += 2 * distance / (final_velocity + self.current_velocity)
        self.current_distance += distance
        self.current_velocity = final_velocity
        return self.current_time, self.current_distance
