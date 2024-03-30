from .node import Node


class YieldSign(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.intersection_occupied = False

    def step(self):
        if self.intersection_occupied:
            self.entry_velocity = 0
        else:
            self.entry_velocity = None
