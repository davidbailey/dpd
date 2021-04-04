from .segment import Segment


class Lane(Segment):
    def __init__(self, link, segment_number):
        super().__init__(link, segment_number)
