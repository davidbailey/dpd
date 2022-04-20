from astropy import units


class SimulatedKinematicBody:
    """
    A class to simulate a kinematic body. Provides methods to move the body with constant velocity.
    """

    def __init__(self, *args, **kwargs):

        self.current_time = 0 * units.second
        self.current_distance = 0 * units.meter
        self.current_velocity = 0 * units.meter / units.second
        self.delta_time = 1 * units.second
        super().__init__(*args, **kwargs)

    def step_velocity(self, write):
        return self.current_velocity

    def step_time(self, write):
        next_time = self.current_time + self.delta_time
        if write:
            self.current_time = next_time
        return next_time

    def step_distance(self, write):
        next_distance = (
            self.current_distance + self.step_velocity(write) * self.delta_time
        )
        if write:
            self.current_distance = next_distance
        return next_distance

    def step(self, write=True):
        next_time = self.step_time(write=write)
        next_distance = self.step_distance(write=write)
        return next_time, next_distance
