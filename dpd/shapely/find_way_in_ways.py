from itertools import combinations

from shapely.geometry import LineString
from shapely.ops import linemerge


def find_way_in_ways(ways, points, buffer_distance=None):
    ways = linemerge(ways)
    for i in range(1, len(ways) + 1):
        for linestring in combinations(ways, i):
            linestring = linemerge(linestring)
            if isinstance(linestring, LineString):
                if buffer_distance:
                    if all(
                        [
                            linestring.intersects(
                                point.location.buffer(buffer_distance)
                            )
                            for point in points
                        ]
                    ):
                        return linestring
                else:
                    if all([linestring.intersects(point.location) for point in points]):
                        return linestring
