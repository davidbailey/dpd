from astropy import units
from pandas import DataFrame

from dpd.mechanics import SimulatedDynamicBody


class DynamicVehicle(DynamicBody):
    """
    Describes a rail or road vehicle and includes methods to drive it along a line
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def drive_between_stops(
        self, speed_limits, distances
    ):  # figure out what to do with speed_limits
        output = []
        segments = list(zip(distances, speed_limits))
        segments.append((0 * units.meter, 0 * units.meter / units.second))
        for _ in range(len(segments) - 1):
            current_segment = segments.pop(0)
            distance = 0 * units.meter
            while distance < current_segment[0]:
                stopping_distance_available = current_segment[0].copy() - distance
                for segment in segments:
                    if self.stopping_distance(
                        segment[1].copy()
                    ) > stopping_distance_available - self.step_distance(write=False):
                        distance += self.decelerate(
                            current_segment[0].copy() - distance, segment[1].copy()
                        )[1]
                        break
                    stopping_distance_available += segment[0].copy()
                if distance == current_segment[0]:
                    break
                distance += self.step_distance(write=True)
            output.append(
                {
                    "time": self.current_time.copy(),
                    "distance": self.current_distance.copy(),
                    "velocity": self.current_velocity.copy(),
                }
            )
            return DataFrame(output)
