from numpy import inf, minimum

from dpd.mechanics import KinematicBody


class KinematicBodyDriver(KinematicBody):
    def __init__(self, segments, *args, **kwargs):
        """
        segments (list of dict): a list of dictionaries of distances (int or float) and (optionally) speed limits (int or float) for segments along a route.
        """
        # can add a warning if max_position is in kwargs
        super().__init__(max_position = 0, *args, **kwargs)
        self.segments = segments
        self.begin_next_segment()

    def begin_next_segment(self):
        self.current_segment = self.segments.pop(0)
        self.max_position += self.current_segment["distance"]
        self.velocity = minimum(
            self.initial_velocity, self.current_segment.get("speed_limit", inf)
        )

    def end_driver(self):
        self.model.schedule.remove(self)

    def driver_step(self):
        if self.position == self.max_position:
            if len(self.segments) > 0:
                self.begin_next_segment()
            else:
                self.end_driver()

    def step(self):
        self.driver_step()
        super().step()
