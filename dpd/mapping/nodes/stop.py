from mesa import Agent

from .node import Node


class Stop(Node, Agent):
    """
    train station, bus stop
    """

    def __init__(self, dwell_time, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.entry_velocity = 0
        self.dwell_time = dwell_time
        self.queue = {}

    def new_approaching_body(self, body):
        if body.unique_id not in self.queue:
            self.queue[body.unique_id] = {
                "dwell_time_remaining": self.dwell_time,
                "body": body,
            }

    def step(self):
        unique_id_to_del = []
        for unique_id in self.queue:
            self.queue[unique_id]["dwell_time_remaining"] -= 1
            if self.queue[unique_id]["dwell_time_remaining"] == 0:
                self.queue[unique_id]["body"].end_current_node()
                unique_id_to_del.append(unique_id)
        for unique_id in unique_id_to_del:
            del self.queue[unique_id]
