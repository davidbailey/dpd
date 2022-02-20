import numpy as np
import pandas as pd


class Vehicle:
    """
    Describes a rail or road vehicle and includes methods to drive it along a line
    """

    def __init__(self, max_speed, max_acceleration, max_deceleration):
        self.max_speed = max_speed
        self.acceleration = max_acceleration
        self.deceleration = max_deceleration

    def accelerate_or_decelerate(self, distance, acceleration_or_deceleration, index):
        """
        Add a segment with constant acceleration (or deceleration
        """
        speed_before_segment = self.speed
        self.speed = np.sqrt(
            speed_before_segment**2 + 2 * acceleration_or_deceleration * distance
        )
        time = (self.speed - speed_before_segment) / acceleration_or_deceleration
        self.segments.append(
            {
                "speed_before_segment": speed_before_segment,
                "speed_after_segment": self.speed,
                "distance": distance,
                "time": time,
                "acceleration": acceleration_or_deceleration,
                "index": index
            }
        )

    def go(self, distance, index):
        """
        Add a segment with constant speed
        """
        time = distance / self.speed
        self.segments.append(
            {
                "speed_before_segment": self.speed,
                "speed_after_segment": self.speed,
                "distance": distance,
                "time": time,
                "acceleration": 0,
                "index": index
            }
        )

    def accelerate_and_go(self, speed_limit, distance, index):
        """
        The case where the vehicle starts a segment slower than the segment's speed limit.
        Two outcomes: 
        1. the vehicle accelerates to the segment's speed limit and drives at the speed limit
        2. the vehicle accelerates, but does not reach the speed limit.
        """
        accelerate_distance = (speed_limit**2 - self.speed**2) / (
            2 * self.acceleration
        )
        if accelerate_distance <= distance:
            self.accelerate_or_decelerate(accelerate_distance, self.acceleration, index)
            self.speed = speed_limit
            self.go(distance - accelerate_distance, index)
        else:
            self.accelerate_or_decelerate(distance, self.acceleration, index)

    def accelerate_and_decelerate(self, speed, distance, speed_limit, index):
        """
        The case where the vehicle accelerates and then immediately decelerates.
        This equation comes from setting the final speed of the acceleration section equal to the initial speed of the deceleration section.
        And setting distance = acceleration distance + deceleration distance. And then solving for deceleration distance.
        """
        deceleration_distance = (speed_limit**2 - speed**2 - 2 * self.acceleration * distance) / (2 * (self.deceleration - self.acceleration))
        self.accelerate_or_decelerate(
            distance - deceleration_distance, self.acceleration, index
        )
        self.accelerate_or_decelerate(deceleration_distance, self.deceleration, index)

    def fix_overspeed(self, speed_limit, distance, index, fix_overspeed_distance=0):
        last_segment = self.segments.pop()
        fix_overspeed_distance = fix_overspeed_distance + last_segment["distance"]
        if speed_limit**2 > last_segment[
            "speed_before_segment"
        ] ** 2 + 2 * self.deceleration * (fix_overspeed_distance):
            self.accelerate_and_decelerate(
                last_segment["speed_before_segment"],
                fix_overspeed_distance,
                speed_limit,
                index
            )
        else:
            self.fix_overspeed(speed_limit, 0, index, fix_overspeed_distance)
        self.speed = speed_limit
        if distance:
            self.go(distance, index)

    def drive_single_segment(self, speed_limit, distance, index):
        """
        Drives a single segment. Three outcomes: 1. Acceleration 2. Constant speed 3. Speed is greater than the Speed Limit and will be fixed.
        """
        speed_limit = min(speed_limit, self.max_speed)
        if self.speed < speed_limit:
            self.accelerate_and_go(speed_limit, distance, index)
        elif self.speed == speed_limit:
            self.go(distance, index)
        if self.speed > speed_limit:
            self.fix_overspeed(speed_limit, distance, index)

    def drive_between_stops(self, speed_limits, lengths):
        """
        Kicks off a drive.
        """
        self.speed = 0
        self.segments = []
        for i in range(len(speed_limits)):
            self.drive_single_segment(speed_limits[i], lengths[i], i)
        self.result = pd.DataFrame(self.segments)
        return self.result
