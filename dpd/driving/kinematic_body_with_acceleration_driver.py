import numpy

from dpd.mechanics import KinematicBodyWithAcceleration
from .kinematic_body_driver import KinematicBodyDriver

class KinematicBodyWithAccelerationDriver(KinematicBodyWithAcceleration, KinematicBodyDriver):
    def __init__(self, driver_max_velocity=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver_max_velocity = driver_max_velocity
        if self.final_velocity:
            self.speed_limits[-1] = self.final_velocity
            
    def begin_next_segment(self):
        self.max_position = self.cumulative_distances[self.route_segment]
        self.acceleration = self.initial_acceleration
        if self.driver_max_velocity is not None:
            self.max_velocity = numpy.minimum(self.speed_limits[self.route_segment], self.driver_max_velocity)
        else:
            self.max_velocity = self.speed_limits[self.route_segment]
        self.final_velocity = self.speed_limits[self.route_segment + 1]


