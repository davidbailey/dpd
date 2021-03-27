class StopIntersection(Intersection):
    """
    🛑 Two-way and four-way stop intersections are the same. The only difference is if some lanes have priority over the stop sign (lanes_with_priority).
    """
    def __init__(self, model, name, geometry):
        super(StopIntersection, self).__init__(model, name, geometry)
        self.lanes_with_priority = [] 
        self.intersection_clear = True

    def add_input_lane(self, input_lane, priority=False):
        self.input_lanes.append(input_lane)
        if priority:
            self.lanes_with_priority.append(input_lane)

    def step(self):
        self.intersection_clear = True

    def new_approach(self, approacher):
        if approacher.lane in self.lanes_with_priority:
            #print(approacher.name, "We have priority. We are going.")
            approacher.proceed_through_intersection()
            self.intersection_clear = False
        elif self.intersection_clear:
            #print(approacher.name, "Intersection clear. We are going.")
            approacher.proceed_through_intersection()
            self.intersection_clear = False
        else:
            #print(approacher.name, "🛑")
            approacher.stop()

