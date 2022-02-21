from numpy import sqrt
from shapely.geometry import LineString

from dpd.geometry import draw_arc


class CurvedSection:
    """
    a curved section
    start_point (Point): the start point of the section
    end_point (Point): the end point of ths section
    radius_of_curvature (float): the Radius of Curvature of the section
    max_cant: (float): the maximum allowable cant (in meters)
    max_cant_deficiency (float): the maximum allowable cant deficiency (in meters)
    gague (float): the track gague (in meters)
    """

    def __init__(
        self,
        start_point,
        end_point,
        radius_of_curvature,
        right_handed,
        max_cant=0.1524,
        max_cant_deficiency=0.075,
        gague=1.435,
        number_of_points=16,
    ):
        self.geometry = LineString(
            draw_arc(
                (start_point.coords[0]),
                (end_point.coords[0]),
                radius_of_curvature,
                right_handed=right_handed,
                number_of_points=number_of_points,
            )
        )
        self.speed_limit = sqrt(
            9.8 * (max_cant + max_cant_deficiency) * radius_of_curvature / gague
        )
