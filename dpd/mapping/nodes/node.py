from mesa import Agent


class Node(Agent):
    """
    A node.
    """
    def __init__(self, geometry, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry = geometry
        self.entry_velocity = None

    def new_approaching_body(self, body):
        body.end_current_node()
