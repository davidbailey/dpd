from .edges_driver import EdgesDriver


class EdgesLanesDriver(EdgesDriver):
    def __init__(self, lane=0, *args, **kwargs):
        self.lane = lane
        super().__init__(*args, **kwargs)

    def begin_next_edge(self, *args, **kwargs):
        super().begin_next_edge(*args, **kwargs)
        self.current_edge.lanes[self.lane].append(self)

    def end_current_edge(self, *args, **kwargs):
        self.current_edge.lanes[self.lane].remove(self)
        if len(self.current_edge.lanes[self.lane]) > 0:
            body_behind_me = self.current_edge.lanes[self.lane][0]
            body_behind_me.max_position = (
                self.body.max_position
            )  # add a stopping distance (and body length) here
        super().end_current_edge(*args, **kwargs)

    def lane_change(self, direction=1):
        self.current_edge.lanes[self.lane].remove(self)
        self.lane += direction
        self.current_edge.lanes[self.lane].append(self)

    def step(self):
        """
        my_index = self.current_edge.lanes[self.lane].index(self)
        if my_index > 0:
            if self.lane < len(self.current_edge.lanes) - 1:
                self.change_lane()
            # there are bodies in front of us, need to check their position
            body_in_front_of_me = self.current_edge.lanes[self.lane][my_index - 1]
            self.max_position = numpy.min([self.max_position, body_in_front_of_me.position])
        """
        super().step()
