from .segment import Segment


class Cycleway(Segment):
    def __init__(self, link, segment_number):
        super().__init__(link, segment_number)
