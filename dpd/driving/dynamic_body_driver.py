import numpy

from dpd.mechanics import DynamicBody
from .driving import KinematicBodyWithAccelerationDriver

class DynamicBodyDriver(DynamicBody, KinematicBodyWithAccelerationDriver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def begin_next_segment(self):
        self.max_position = self.cumulative_distances[self.route_segment]
        if self.driver_max_velocity is not None:
            self.max_velocity = numpy.minimum(self.speed_limits[self.route_segment], self.driver_max_velocity)
        else:
            self.max_velocity = self.self.speed_limits[self.route_segment]
        self.final_velocity = self.self.speed_limits[self.route_segment + 1]


