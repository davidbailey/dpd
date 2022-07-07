from astropy import units

from .one_dimensional_body import OneDimensionalBody

class SimulatedKinematicBody(OneDimensionalBody:
    """
    A class to simulate a kinematic body. Provides methods to move the body with constant velocity.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = 0 * units.meter / units.second

    def step_position(self):
        self.position = self.position + self.velocity
        return self.position
