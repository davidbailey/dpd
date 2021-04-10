from dpd.modeling.agents.intersections.yield_intersection import YieldIntersection
from dpd.modeling.agents.intersections.stop_intersection import StopIntersection
from dpd.modeling.agents.intersections.signal_intersection import SignalIntersection

from .agent_based_dict import AgentBasedDict


class AgentBasedIntersections(AgentBasedDict):
    """
    A container for agent-based Intersections
    """

    def __init__(self, data={}, crs=None, *args, **kwargs):
        super().__init__(data=data, crs=crs, *args, **kwargs)
        for key, intersection in self.items():
            if hasattr(intersection, "type_"):
                intersection_type = intersection["type_"]
                if intersection_type == "Signal":
                    self.intersections[key] = SignalIntersection(
                        intersection, self.model
                    )
                elif intersection_type == "Stop":
                    self.intersections[key] = StopIntersection(intersection, self.model)
                else:
                    self.intersections[key] = YieldIntersection(
                        intersection, self.model
                    )
            else:
                self.intersections[key] = YieldIntersection(intersection, self.model)
            self.model.schedule.add(self.intersections[key])
