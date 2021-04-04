from .segment import Segment

class Sidewalk(Segment):
    def __init__(self, link, segment_number):
        super().__init__(link, segment_number)
