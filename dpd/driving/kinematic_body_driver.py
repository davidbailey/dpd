import numpy

from dpd.mechanics import KinematicBody

class KinematicBodyDriver(KinematicBody):
    def __init__(self, distances, speed_limits=None, *args, **kwargs):
        """
        distances (list): a list of numbers (int, float, array) of distances for segments along a route.
        speed_limits (list): a corresponding list (int, float, array) of speed limits for segments along a route.
        """
        self.distances = distances
        self.distances.append(0 * distances[0])
        self.speed_limits = speed_limits
        self.speed_limits.append(0 * speed_limits[0])
        self.cumulative_distances = numpy.cumsum(self.distances)
        self.route_segment = 0
        super().__init__(*args, **kwargs)
            
    def begin_next_segment(self):
        self.max_position = self.cumulative_distances[self.route_segment]
        if speed_limits is not None:
            self.velocity = numpy.minimum(self.initial_velocity, self.speed_limits[self.route_segment])

    def driver_step(self):
        if self.position == self.cumulative_distances[self.route_segment]:
            if self.route_segment < len(self.route) - 2:
                self.route_segment += 1
                self.begin_next_segment()
            else:
                self.model.schedule.remove(self)  # this works great, except we don't get datacollection on the last step

    def step(self):
        super().step()
        self.driver_step()


