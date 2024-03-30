from .node import Node


class StopSign(Node):
    def __init__(self, entry_velocity = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry_velocity = entry_velocity
