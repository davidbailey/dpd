from astropy import units
import pandas as pd


class ConstantSpeedVehicle:
    """
    Describes a rail or road vehicle and includes methods to drive it along a line
    """

    def __init__(self, max_speed, max_acceleration=None, max_deceleration=None):
        self.max_speed = max_speed * units.meter / units.second

    def go(self, distance, speed):
        """
        Add a segment with constant speed
        """
        time = distance / speed
        self.segments.append(
            {
                "speed": speed,
                "distance": distance,
                "time": time,
            }
        )

    def drive_single_segment(self, speed_limit, distance):
        """
        Drives a single segment.
        """
        speed = min(speed_limit, self.max_speed)
        self.go(distance, speed)

    def drive_between_stops(self, speed_limits, lengths):
        """
        Kicks off a drive.
        """
        self.segments = []
        for i in range(len(speed_limits)):
            self.drive_single_segment(speed_limits[i], lengths[i])
        self.result = pd.DataFrame(self.segments)
        return self.result
