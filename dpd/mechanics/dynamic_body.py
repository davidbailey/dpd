from astropy import units
from pandas import DataFrame

class DynamicBody:
    """
    This model represents a constant-power dynamic body moving in one dimension with a constant deceleration.
    power = mass * acceleration * velocity
    """
    def __init__(
        self,
        power, 
        mass, 
        max_speed, 
        max_acceleration,
        max_deceleration, 
        initial_time = None,
        initial_distance = None, 
        initial_speed = None 
    ):
        self.power = power
        self.mass = mass
        self.max_speed = max_speed
        self.max_acceleration = max_acceleration
        self.max_deceleration = max_deceleration
        if initial_time:
            self.current_time = initial_time
        else:
            self.current_time = 0 * units.second
        if initial_distance:
            self.current_distance = initial_distance
        else:
            self.current_distance = 0 * units.meter
        if initial_speed:
            self.current_speed = initial_speed
        else:
            self.current_speed = 0 * units.meter / units.second
    
    @property
    def acceleration(self):
        """
        The issue here is that acceleration = power / (mass * velocity). So if velocity=0,
        then acceleration is infinite, which is a problem.
        """
        return min(self.power / (self.mass * self.current_speed), self.max_acceleration)

    def stopping_distance(self, final_speed):
        return (final_speed**2 - self.current_speed**2) / (2 * self.max_deceleration)

    def step_speed(self, speed_limit, time_delta):
        speed = self.current_speed + self.acceleration * time_delta
        return min(self.max_speed, speed_limit, speed)

    def step_distance(self, speed_limit, time_delta, write):
        if write:
            self.current_time += time_delta
            self.current_speed = self.step_speed(speed_limit, time_delta)
            self.current_distance += self.step_speed(speed_limit, time_delta) * time_delta
        return self.step_speed(speed_limit, time_delta) * time_delta

    def decelerate(self, distance, speed):
        self.current_time += 2 * distance / (speed + self.current_speed)
        self.current_speed = speed
        self.current_distance += distance
        return distance

    def drive_segments(self, distances, speed_limits, time_delta):
        output = []
        segments = list(zip(distances, speed_limits))
        segments.append((0 * units.meter, 0 * units.meter / units.second))
        for _ in range(len(segments) - 1):
            current_segment = segments.pop(0)
            distance = 0 * units.meter
            while distance < current_segment[0]:
                stopping_distance_available = current_segment[0].copy() - distance
                for segment in segments:
                    if self.stopping_distance(segment[1].copy()) > stopping_distance_available - self.step_distance(current_segment[1].copy(), time_delta, False):
                        distance += self.decelerate(current_segment[0].copy() - distance, segment[1].copy())
                        break
                    stopping_distance_available += segment[0].copy()
                if distance == current_segment[0]:
                    break
                distance += self.step_distance(current_segment[1].copy(), time_delta, True)
            output.append({
                "time": self.current_time.copy(),
                "distance": self.current_distance.copy(),
                "speed": self.current_speed.copy(),
            })
        return DataFrame(output)
