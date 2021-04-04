from .segment import Segment
from dpd.modeling.agents.people import Cyclist, Pedestrian

class Cycleway(Segment):
    def __init__(self, link, segment_number):
        super().__init__(link, segment_number)
        self.allowed_users = [Cyclist, Pedestrian] # move to modeling
