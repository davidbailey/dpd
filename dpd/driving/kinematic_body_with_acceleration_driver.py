from numpy import inf, minimum, sqrt

from dpd.mechanics import KinematicBodyWithAcceleration

from .kinematic_body_driver import KinematicBodyDriver


class KinematicBodyWithAccelerationDriver(
    KinematicBodyWithAcceleration, KinematicBodyDriver
):
    def __init__(self, driver_max_velocity=None, *args, **kwargs):
        self.driver_max_velocity = driver_max_velocity
        super().__init__(*args, **kwargs)
        if self.segments[0].get("speed_limit"):
            self.check_stopping_distance_speed_limits()
        if self.final_velocity is not None:
            self.segments.append({"distance": 0, "speed_limit": self.final_velocity})

    def check_stopping_distance_speed_limits(self):
        """
        It is highly possible that the distances and speed_limits do not sufficiently allow for a body to stop (and this depends on the max_deceleration of the body, not the distance/speed_limit).
        (e.g. if you have a body traveling at 50 m/s and the last distance is 1m, the body would require a very high max_deceleration to stop.)
        e.g. distances = [100m, 100m, 1m, 0m] speed_limits = [50m/s, 50m/s, 50m/s, 0m/s]
        we need to update speed_limit[2] from 50m/s to a speed such SPEED that the body can get to 0m/s from SPEED within 1m.
        """
        for i in range(len(self.segments) - 1, 0, -1):
            stopping_distance_speed_limit = sqrt(
                self.segments[i]["speed_limit"] ** 2
                + 2 * self.max_deceleration * self.segments[i - 1]["distance"]
            )
            self.segments[i - 1]["speed_limit"] = minimum(
                self.segments[i - 1]["speed_limit"], stopping_distance_speed_limit
            )

    def begin_next_segment(self):
        self.max_position = self.current_segment["cumulative_distance"]
        # note, this is ok in DynamicBodyDriver because a DynamicBody will reset this before we accelerate
        self.acceleration = self.initial_acceleration
        speed_limit = self.current_segment.get("speed_limit", inf)
        if self.driver_max_velocity is not None:
            self.max_velocity = minimum(speed_limit, self.driver_max_velocity)
        else:
            self.max_velocity = speed_limit
        if len(self.segments) > 0 and self.segments[0].get("speed_limit"):
            self.final_velocity = self.segments[0]["speed_limit"]
