import numpy

from .kinematic_body_with_acceleration_driver import KinematicBodyWithAccelerationDriver


class KinematicBodyWithAccelerationStopper(KinematicBodyWithAccelerationDriver):
    def __init__(self, segments=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments = segments
        self.dwell_time = 1 * self.model.time_unit
        self.stop_name = None

    def end_driver(self):
        if self.segments:
            current_segment = self.segments.pop(0)
            if "distances" in current_segment:
                self.distances = current_segment["distances"]
                if "speed_limits" in current_segment:
                    self.speed_limits = current_segment["speed_limits"]
                    # need to stop..
                    self.distances = numpy.concatenate((self.distances, [0]))
                    self.speed_limits = numpy.concatenate((self.speed_limits, [0]))
                else:
                    self.speed_limits = None
                self.cumulative_distances = numpy.cumsum(self.distances) + self.position
                self.begin_next_segment()
            elif "dwell_time" in current_segment:
                self.dwell_time = current_segment["dwell_time"]
                if "stop_name" in current_segment:
                    self.stop_name = current_segment["stop_name"]
        else:
            self.model.schedule.remove(self)

    def step(self):
        if self.dwell_time is not None:
            self.dwell_time = self.dwell_time - 1 * self.model.time_unit
            if self.dwell_time <= 0 * self.model.time_unit:
                self.dwell_time = None
                self.stop_name = None
                self.end_driver()
        else:
            super().step()
