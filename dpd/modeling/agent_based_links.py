from dpd.geometry import GeometricDict
from dpd.mapping import Lane, Sidewalk, Cycleway
from dpd.modeling.agents.people import Cyclist, Driver, Pedestrian


class AgentBasedLinks(GeometricDict):
    """
    A continer for agent-based Links
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for link in self.values():
            link.length = link.geometry.length
            for segment in link.segments:
                if type(segment) in [Lane]:
                    segment.allowed_users = [Cyclist, Pedestrian, Driver]
                elif type(segment) in [Sidewalk, Cycleway]:
                    segment.allowed_users = [Cyclist, Pedestrian]
        self.clear_all_segments()

    def update_intersections(self, intersections):
        """This method is redundant to Intersections.update_links. Call one or the other."""
        for link in self.values():
            if link.input_intersection:
                link.input_intersection = intersections[link.input_intersection.name]
            if link.output_intersection:
                link.output_intersection = intersections[link.output_intersection.name]

    def clear_all_segments(self):
        """
        adds occupants to all segments. can also be run later to clear segments of occupants from past model
        """
        for link in self.values():
            for segment in link.segments:
                if segment is not None:
                    segment.occupants = []
