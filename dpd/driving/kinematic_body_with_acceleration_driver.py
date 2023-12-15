import numpy

from dpd.mechanics import KinematicBodyWithAcceleration

from .kinematic_body_driver import KinematicBodyDriver


class KinematicBodyWithAccelerationDriver(
    KinematicBodyWithAcceleration, KinematicBodyDriver
):
    def __init__(self, driver_max_velocity=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver_max_velocity = driver_max_velocity
        if self.final_velocity is not None:
            self.distances = numpy.concatenate((self.distances, [0]))
            self.speed_limits = numpy.concatenate((self.speed_limits, [0]))
            self.speed_limits[-1] = self.final_velocity

    def check_stopping_distance_speed_limits(self):
        """
        It is highly possible that the distances and speed_limits do not sufficiently allow for a body to stop (and this depends on the max_deceleration of the body, not the distance/speed_limit).
        (e.g. if you have a body traveling at 50 m/s and the last distance is 1m, the body would require a very high max_deceleration to stop.)
        e.g. distances = [100m, 100m, 1m, 0m] speed_limits = [50m/s, 50m/s, 50m/s, 0m/s]
        we need to update speed_limit[2] from 50m/s to a speed such SPEED that the body can get to 0m/s from SPEED within 1m.
        """
        for i in range(len(self.speed_limits) - 1, 0, -1):
            stopping_distance_speed_limit = numpy.sqrt(
                self.speed_limits[i] ** 2
                + 2 * self.max_deceleration * self.distances[i - 1]
            )
            self.speed_limits[i - 1] = numpy.minimum(
                self.speed_limits[i - 1], stopping_distance_speed_limit
            )

    def begin_next_segment(self):
        self.max_position = self.cumulative_distances[0]
        self.cumulative_distances = self.cumulative_distances[1:]
        # note, this is ok in DynamicBodyDriver because a DynamicBody will reset this before we accelerate
        self.acceleration = self.initial_acceleration
        if self.speed_limits and len(self.speed_limits) > 0:
            self.check_stopping_distance_speed_limits()
            speed_limit = self.speed_limits[0]
            self.speed_limits = self.speed_limits[1:]
            if self.driver_max_velocity is not None:
                self.max_velocity = numpy.minimum(speed_limit, self.driver_max_velocity)
            else:
                self.max_velocity = speed_limit
        else:
            if self.driver_max_velocity is not None:
                self.max_velocity = self.driver_max_velocity
            else:
                self.max_velocity is None
        if self.speed_limits and len(self.speed_limits) > 0:
            self.final_velocity = self.speed_limits[0]
