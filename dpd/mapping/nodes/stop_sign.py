from mesa import Agent

from .node import Node


class StopSign(Node, Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry_velocity = 0
