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

    def accelerate_or_decelerate(self, distance, acceleration_or_deceleration, speed_limit):
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
                "speed_limit": speed_limit,
                "distance": distance,
                "time": time,
                "acceleration": acceleration_or_deceleration,
            }
        )

    def go(self, distance):
        """
        Add a segment with constant speed
        """
        if distance == 0:
            time = 0
        else:
            time = distance / self.speed
        self.segments.append(
            {
                "speed_before_segment": self.speed,
                "speed_after_segment": self.speed,
                "speed_limit": self.speed,
                "distance": distance,
                "time": time,
                "acceleration": 0,
            }
        )

    def accelerate_and_go(self, speed_limit, distance):
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
            self.accelerate_or_decelerate(accelerate_distance, self.acceleration, speed_limit)
            self.speed = speed_limit
            self.go(distance - accelerate_distance)
        else:
            self.accelerate_or_decelerate(distance, self.acceleration, speed_limit)

    def accelerate_go_and_decelerate(self, speed, distance, intermediate_speed_limit, final_speed_limit):
        """
        There are two cases:
        1. The vehicle never reaches the speed limit of the segment: it accelerates and then decelerates.
        2. The vehicle reaches the speed limit of segment: it accelerates, goes at the speed limit, then decelerates.
        This equation comes from setting the final speed of the acceleration section equal to the initial speed of the deceleration section.
        And setting distance = acceleration distance + deceleration distance. And then solving for deceleration distance.
        """
        deceleration_distance = (final_speed_limit**2 - speed**2 - 2 * self.acceleration * distance) / (2 * (self.deceleration - self.acceleration))
        if np.sqrt(speed**2 + 2 * self.acceleration * (distance - deceleration_distance)) <= intermediate_speed_limit: 
            self.accelerate_or_decelerate(
                distance - deceleration_distance, self.acceleration, intermediate_speed_limit
            )
            self.accelerate_or_decelerate(deceleration_distance, self.deceleration, intermediate_speed_limit)
        else:
            deceleration_distance = (final_speed_limit**2 - intermediate_speed_limit**2) / (2 * self.acceleration)
            self.accelerate_and_go(intermediate_speed_limit, distance - deceleration_distance)
            self.accelerate_or_decelerate(deceleration_distance, self.deceleration, intermediate_speed_limit)

    def fix_overspeed(self, speed_limit, distance, fix_overspeed_distance=0):
        """
        Fix the case the vehicle gets to a segment and is going too fast.
        Remove the last segment and use that distance to decelerate. Two cases:
        1. There is enough distance to slow down.
        2. There is not enough distance to slow down: repeat the process.
        In either case, the vehicle will travel the next segment at that segment's speed limit.
        """
        last_segment = self.segments.pop()
        fix_overspeed_distance = fix_overspeed_distance + last_segment["distance"]
        if speed_limit**2 > last_segment[
            "speed_before_segment"
        ] ** 2 + 2 * self.deceleration * (fix_overspeed_distance):
            self.accelerate_go_and_decelerate(
                last_segment["speed_before_segment"],
                fix_overspeed_distance,
                last_segment["speed_limit"],
                speed_limit,
            )
        else:
            self.fix_overspeed(speed_limit, 0, fix_overspeed_distance)
        self.speed = speed_limit
        if distance:
            self.go(distance)

    def drive_single_segment(self, speed_limit, distance):
        """
        Drives a single segment. Three outcomes: 1. Acceleration 2. Constant speed 3. Speed is greater than the Speed Limit and will be fixed.
        """
        speed_limit = min(speed_limit, self.max_speed)
        if self.speed < speed_limit:
            self.accelerate_and_go(speed_limit, distance)
        elif self.speed == speed_limit:
            self.go(distance)
        if self.speed > speed_limit:
            self.fix_overspeed(speed_limit, distance)

    def drive_between_stops(self, speed_limits, lengths):
        """
        Kicks off a drive.
        """
        self.speed = 0
        self.segments = []
        for i in range(len(speed_limits)):
            self.drive_single_segment(speed_limits[i], lengths[i])
        self.result = pd.DataFrame(self.segments)
        return self.result
