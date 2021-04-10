from dpd.modeling.agents.intersections.yield_intersection import YieldIntersection

# from dpd.modeling.agents.intersections.stop_intersection import StopIntersection
# from dpd.modeling.agents.intersections.signal_intersection import SignalIntersection

from .agent_based_dict import AgentBasedDict

StopIntersection = YieldIntersection
SignalIntersection = YieldIntersection


class AgentBasedIntersections(AgentBasedDict):
    """
    A container for agent-based Intersections
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, intersection in self.items():
            if hasattr(intersection, "type_"):
                intersection_type = intersection["type_"]
                if intersection_type == "Signal":
                    self[key] = SignalIntersection(intersection, self.model)
                elif intersection_type == "Stop":
                    self[key] = StopIntersection(intersection, self.model)
                else:
                    self[key] = YieldIntersection(intersection, self.model)
            else:
                self[key] = YieldIntersection(intersection, self.model)
            self.model.schedule.add(self[key])
