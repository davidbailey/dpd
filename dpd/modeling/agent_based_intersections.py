from dpd.modeling.agents.intersections.yield_intersection import YieldIntersection

from dpd.modeling.agents.intersections.stop_intersection import StopIntersection

# from dpd.modeling.agents.intersections.signal_intersection import SignalIntersection

from .agent_based_dict import AgentBasedDict

SignalIntersection = YieldIntersection


class AgentBasedIntersections(AgentBasedDict):
    """
    A container for agent-based Intersections
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, intersection in self.items():
            if hasattr(intersection, "type_"):
                intersection_type = intersection.type_
                if intersection_type == "Signal":
                    self[key] = SignalIntersection(intersection, self.model)
                elif intersection_type == "Stop":
                    self[key] = StopIntersection(intersection, self.model)
                else:
                    self[key] = YieldIntersection(intersection, self.model)
            else:
                self[key] = YieldIntersection(intersection, self.model)
            self.model.schedule.add(self[key])

    def update_links(self, links):
        """This method is redundant to Links.update_intersections. Call one or the other."""
        for intersection in self.values():
            for link in intersection.input_links:
                link.output_intersection = self
            for link in intersection.output_links:
                link.input_intersection = self

    def nodes_to_links(self, node_ids):
        """Takes a list of node_ids and a map and returns a list or links."""
        nodes = []
        # first we filter through all the nodes and find those that are actually intersections. for those that are not intersections, we assume they are part of the links. this may or may not be true.
        for node in node_ids:
            if node in self.keys():
                nodes.append(node)
        links = []
        for i in range(len(nodes) - 1):
            for link in self[nodes[i]].output_links:
                if (
                    link.output_intersection
                    and link.output_intersection.name == nodes[i + 1]
                ):
                    links.append(link)
                    break
        return links
