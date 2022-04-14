from astropy import units

from .simulated_kinematic_body import SimulatedKinematicBody


class SimulatedKinematicBodyWithAcceleration(SimulatedKinematicBody):
    """
    A class to simulate a kinematic body. Provides methods to move the body with constant acceleration.
    """

    def __init__(
        self,
        initial_acceleration=0 * units.meter / units.second**2,
        velocity_limit=None,
        *args,
        **kwargs
    ):
        self.current_acceleration = initial_acceleration
        self.velocity_limit = velocity_limit
        super().__init__(*args, **kwargs)

    def step_acceleration(self, write):
        return self.current_acceleration

    def step_velocity(self, write):
        next_velocity = (
            self.current_velocity + self.step_acceleration(write) * delta_time
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
