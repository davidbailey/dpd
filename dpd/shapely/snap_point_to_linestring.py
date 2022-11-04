from shapely.geometry import LineString
from shapely.ops import linemerge

from .cut import cut


def snap_point_to_linestring(linestring, point):
    """
    "Snaps the point to the closest point along the linestring. Adds that point to the linestring. Returns the new linestring and the closest point on the linestring.
    """
    distance = linestring.project(point)
    closest_point_on_linestring = linestring.interpolate(distance)
    new_linestring = linemerge(cut(linestring, distance))
    return new_linestring, closest_point_on_linestring
