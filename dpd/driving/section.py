from numpy import sqrt
from shapely.geometry import LineString

from dpd.analysis.costs import segment_cost, modes, elevations
from dpd.geometry import draw_arc


class Section:
    """
    a section of a route: curved section (if there is a radius_of_curvature) or straight section
    start_point (Point): the start point of the section
    end_point (Point): the end point of ths section
    radius_of_curvature (float): the Radius of Curvature of the section (in meters)
    """

    def __init__(
        self,
        start_point,
        end_point,
        radius_of_curvature=None,
        right_handed=True,
        number_of_points=16,
        elevation="surface",
        mode="rail",
    ):
        if elevation not in elevations:
            raise ValueError("elevation must be one of " + str(elevations))
        if mode not in mode:
            raise ValueError("mode must be one of " + str(modes))
        self.elevation = elevation
        self.radius_of_curvature = radius_of_curvature
        if radius_of_curvature:
            self.geometry = LineString(
                draw_arc(
                    (start_point.coords[0]),
                    (end_point.coords[0]),
                    radius_of_curvature,
                    right_handed,
                    number_of_points,
                )
            )
        else:
            self.geometry = LineString([start_point, end_point])

    @property
    def speed_limit(self, max_cant=0.1524, max_cant_deficiency=0.075, gague=1.435):
        """
        max_cant: (float): the maximum allowable cant (in meters)
        max_cant_deficiency (float): the maximum allowable cant deficiency (in meters)
        gague (float): the track gague (in meters)
        """
        if self.radius_of_curvature:
            return sqrt(
                9.8
                * (max_cant + max_cant_deficiency)
                * self.radius_of_curvature
                / gague
            )
        else:
            return None

    @property
    def cost(self):
        return segment_cost(self.mode, self.elevation, self.geometry.length)
