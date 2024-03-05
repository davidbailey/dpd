from mesa import Agent

from .node import Node


class YieldSign(Node, Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.intersection_occupied = False

    def step(self):
        if intersection_occupied:
            self.entry_velocity = 0
        else:
            self.entry_velocity = None
