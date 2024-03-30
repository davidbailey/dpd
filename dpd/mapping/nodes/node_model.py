from uuid import uuid4

from mesa import Model
from mesa.time import BaseScheduler

from .node import Node
from .stop import Stop
from .stop_light import StopLight
from .stop_sign import StopSign
from .yield_sign import YieldSign


class NodeModel(Model):
    def __init__(self, velocity_unit=1):
        super().__init__()
        self.schedule = BaseScheduler(self)
        self.velocity_unit = velocity_unit

    def step(self):
        self.schedule.step()

    def object_for_node(self, node):
        unique_id = uuid4()
        if node.get("type") == "stop_sign":
            object = StopSign(
                model=self, unique_id=unique_id, geometry=node["geometry"]
            )
        elif node.get("type") == "yield_sign":
            object = YieldSign(
                model=self, unique_id=unique_id, geometry=node["geometry"]
            )
        elif node.get("type") == "stop_light":
            object = StopLight(
                model=self, unique_id=unique_id, geometry=node["geometry"]
            )
        elif node.get("type") == "stop":
            object = Stop(
                model=self,
                unique_id=unique_id,
                geometry=node["geometry"],
                dwell_time=node["dwell_time"],
                entry_velocity=0 * self.velocity_unit,
            )
        else:
            object = Node(model=self, unique_id=unique_id, geometry=node["geometry"])
        self.schedule.add(object)
        return object
