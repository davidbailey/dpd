import numpy

from dpd.mechanics import KinematicBody


class KinematicBodyDriver(KinematicBody):
    def __init__(self, distances=None, speed_limits=None, *args, **kwargs):
        """
        distances (list): a list of numbers (int, float, array) of distances for segments along a route.
        speed_limits (list): a corresponding list (int, float, array) of speed limits for segments along a route.
        """
        super().__init__(*args, **kwargs)
        self.distances = distances
        self.speed_limits = speed_limits
        self.cumulative_distances = numpy.cumsum(self.distances)

    def begin_next_segment(self):
        self.max_position = self.cumulative_distances[0]
        self.cumulative_distances = self.cumulative_distances[1:]
        if self.speed_limits is not None:
            speed_limit = self.speed_limits[0]
            self.speed_limits = self.speed_limits[1:]
            self.velocity = numpy.minimum(self.initial_velocity, speed_limit)

    def end_driver(self):
        self.model.schedule.remove(self)

    def driver_step(self):
        if self.position == self.max_position:
            if self.cumulative_distances and len(self.cumulative_distances) > 0:
                self.begin_next_segment()
            else:
                self.end_driver()

    def step(self):
        self.driver_step()
        super().step()
