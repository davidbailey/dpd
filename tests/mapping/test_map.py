from itertools import combinations
import unittest

from shapely.geometry import Point, LineString

from dpd.mapping import Intersection, Map, Link


def build_test_map():
    map_ = Map()
    for x in range(2):
        for y in range(2):
            map_.intersections[str([x, y])] = Intersection(str([x, y]), Point(x, y))
    for input_intersection, output_intersection in combinations(
        map_.intersections.values(), 2
    ):
        name = input_intersection.name + " to " + output_intersection.name
        geometry = LineString(
            [input_intersection.geometry, output_intersection.geometry]
        )
        segments = []
        map_.links[name] = Link(
            name,
            geometry,
            segments,
            input_intersection,
            output_intersection,
            number_of_lanes=1,
            sidewalk=True,
            cycleway="track",
            max_speed=25 * units.imperial.mile / units.hour,
        )
        map_.links[name].update_segments_from_osm(
            number_of_lanes=1, sidewalk=True, cycleway="track"
        )
    return map_


class TestMap(unittest.TestCase):
    def test_map(self):
        self.map_ = build_test_map()
        self.map_.plot(include_intersections=True)
        self.map_.links.crs = "EPSG:4326"
        self.map_.intersections.crs = "EPSG:4326"
        self.map_.plot_folium(include_intersections=True)
        self.map_.to_geodigraph()


if __name__ == "__main__":
    unittest.main()
