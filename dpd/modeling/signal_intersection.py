class SignalIntersection(YieldIntersection):
    """
    🚦🚥 We have a signal plan that updates lanes_with_green after time. Traffic follows the signal plan.
    """

    def __init__(self, intersection, model):
        super().__init__(self, intersection, model)
        self.create_signal_plan()
        self.phase = 0
        self.time_in_phase = 0

    def create_signal_plan(self):
        signal_plan = []
        for road in self.input_roads:
            phase = {"time": 5, "lanes_with_green": []}
            for lane in road.lanes:
                phase["lanes_with_green"].append(lane)
        self.signal_plan = signal_plan
        self.lanes_with_green = signal_plan[0]["lanes_with_green"]

    def step(self):
        if self.time_in_phase < self.signal_plan[self.phase]["time"]:
            self.time_in_phase += 1
        else:
            if self.phase < len(self.signal_plan) - 1:
                self.phase += 1
            else:
                self.phase = 0
            self.time_in_phase = 0
            self.lanes_with_green = self.signal_plan[self.phase]["lanes_with_green"]

    def new_approach(self, approacher):
        if approacher.lane in self.lanes_with_green:
            approacher.proceed_through_intersection()
        else:
            approacher.stop()
