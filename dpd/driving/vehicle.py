import numpy as np
import pandas as pd


class Vehicle:
    """
    Describes a rail or road vehicle and includes methods to drive it along a line
    """

    def __init__(self, max_speed, max_acceleration, max_deceleration, name=""):
        self.max_speed = max_speed
        self.acceleration = max_acceleration
        self.deceleration = max_deceleration
        self.name = name

    def accelerate_or_decelerate(self, distance, acceleration_or_deceleration):
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
            }
        )

    def go(self, distance):
        time = distance / self.speed
        self.segments.append(
            {
                "speed_before_segment": self.speed,
                "speed_after_segment": self.speed,
                "distance": distance,
                "time": time,
                "acceleration": 0,
            }
        )

    def accelerate_and_go(self, speed_limit, distance):
        accelerate_distance = (speed_limit**2 - self.speed**2) / (
            2 * self.acceleration
        )
        if accelerate_distance <= distance:
            self.accelerate_or_decelerate(accelerate_distance, self.acceleration)
            self.speed = speed_limit
            self.go(distance - accelerate_distance)
        else:
            self.accelerate_or_decelerate(distance, self.acceleration)

    def accelerate_and_decelerate(self, speed, distance, speed_limit):
        deceleration_distance = (
            2 * self.acceleration * distance + speed**2 - speed_limit**2
        ) / (2 * (self.acceleration - self.deceleration))
        self.accelerate_or_decelerate(
            distance - deceleration_distance, self.acceleration
        )
        self.accelerate_or_decelerate(deceleration_distance, self.deceleration)

    def fix_overspeed(self, speed_limit, distance, fix_overspeed_distance=0):
        last_segment = self.segments.pop()
        fix_overspeed_distance = fix_overspeed_distance + last_segment["distance"]
        if speed_limit**2 > last_segment[
            "speed_before_segment"
        ] ** 2 + 2 * self.deceleration * (fix_overspeed_distance):
            self.accelerate_and_decelerate(
                last_segment["speed_before_segment"],
                fix_overspeed_distance,
                speed_limit,
            )
        else:
            self.fix_overspeed(speed_limit, distance, fix_overspeed_distance)
        self.speed = speed_limit
        self.go(distance)

    def drive_single_segment(self, speed_limit, distance):
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
        list(
            map(
                lambda x: self.drive_single_segment(x[0], x[1]),
                zip(speed_limits, lengths),
            )
        )
        self.result = pd.DataFrame(self.segments)
        return self.result
