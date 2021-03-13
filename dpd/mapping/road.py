class Road:
    """
    Note: the output_intersection of a road means that road is an input_road of that intersection. And the input_intersection of a road means that road is an output_road of that intersection
    """
    def __init__(
        self,
        name,
        geometry,
        input_intersection,
        output_intersection,
        number_of_lanes,
        max_speed=25,
    ):
        self.name = name
        self.geometry = geometry
        self.input_intersection = input_intersection
        if input_intersection:
            input_intersection.add_output_road(self)
        self.output_intersection = output_intersection
        if output_intersection:
            output_intersection.add_input_road(self)
        self.lanes = [None, None]
        for lane_number in range(number_of_lanes):
            lane = Lane(self, lane_number)
            self.lanes.insert(-1, lane)
        self.max_speed = max_speed
