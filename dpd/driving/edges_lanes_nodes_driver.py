from .edges_lanes_driver import EdgesLanesDriver


class EdgesLanesNodesDriver(EdgesLanesDriver):
    def __init__(self, nodes, *args, **kwargs):
        self.nodes = nodes
        self.waiting_at_node = False
        self.begin_next_node()
        super().__init__(*args, **kwargs)

    def begin_next_edge(self, *args, **kwargs):
        super().begin_next_edge(*args, **kwargs)
        if self.next_node.entry_velocity is not None:
            self.body.final_velocity = minimum(
                self.body.final_velocity, self.next_node.entry_velocity
            )

    def end_current_edge(self, *args, **kwargs):
        if not self.waiting_at_node:
            self.waiting_at_node = True
            self.next_node.new_approaching_body(self)

    def begin_next_node(self):
        self.next_node = self.nodes.pop(0)

    def end_current_node(self):
        self.waiting_at_node = False
        self.begin_next_node()
        super().end_current_edge(
            extra_position=None
        )  ## update this in cases where the driver does not stop
