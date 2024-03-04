from numpy import maximum, minimum

from .body import Body


class KinematicBody(Body):
    """
    A class to simulate a kinematic body. Provides methods to move the body with constant velocity.
    """

    def __init__(
        self, initial_velocity, max_position=None, min_position=None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.initial_velocity = initial_velocity
        self.velocity = initial_velocity
        self.max_position = max_position
        self.min_position = min_position

    def step_position(self):
        next_position = self.position + self.velocity * self.model.time_unit
        if self.max_position is not None:
            self.position = minimum(next_position, self.max_position)
            if self.position != next_position:
                return self.position - next_position
        if self.min_position is not None:
            self.position = maximum(next_position, self.min_position)
            if self.position != next_position:
                return next_position - self.position
        self.position = next_position
        return None

    def step(self):
        extra_position = self.step_position()
        super().step()
        return {"extra_position": extra_position}
