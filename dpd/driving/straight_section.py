from shapely.geometry import LineString

class StraightSection:
    """
    a straight section
    start_point (Point): the start point of the section
    end_point (Point): the end point of ths section
    """
    def __init__(
        self,
        start_point,
        end_point,
    ):
        self.geometry = LineString([start_point, end_point])
        self.speed_limit = None
