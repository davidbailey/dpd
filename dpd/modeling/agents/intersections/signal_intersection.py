from .yield_intersection import YieldIntersection


class SignalIntersection(YieldIntersection):
    """
    🚦🚥 We have a signal plan that updates segments_with_green after time. Traffic follows the signal plan.
    """

    def __init__(self, intersection, model):
        super().__init__(self, intersection, model)
        self.create_signal_plan()
        self.phase = 0
        self.time_in_phase = 0

    def create_signal_plan(self):
        signal_plan = []
        for link in self.input_links:
            phase = {"time": 5, "segments_with_green": []}
            for segment in link.segments:
                phase["segments_with_green"].append(segment)
        self.signal_plan = signal_plan
        self.segments_with_green = signal_plan[0]["segments_with_green"]

    def step(self):
        if self.time_in_phase < self.signal_plan[self.phase]["time"]:
            self.time_in_phase += 1
        else:
            if self.phase < len(self.signal_plan) - 1:
                self.phase += 1
            else:
                self.phase = 0
            self.time_in_phase = 0
            self.segments_with_green = self.signal_plan[self.phase][
                "segments_with_green"
            ]

    def new_approach(self, approacher):
        if approacher.segment in self.segments_with_green:
            approacher.proceed_through_intersection()
        else:
            approacher.stop()
