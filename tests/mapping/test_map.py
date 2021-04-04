from itertools import combinations
import unittest

from shapely.geometry import Point, LineString

from dpd.mapping import Intersection, Lane, Road, Map


class TestMap(unittest.TestCase):
    def test_map(self):
        self.map_ = Map()
        for x in range(2):
            for y in range(2):
                self.map_.add_intersection(Intersection(str([x, y]), Point(x, y)))
        for input_intersection, output_intersection in combinations(
            self.map_.intersections["Intersection"], 2
        ):
            name = input_intersection.name + " to " + output_intersection.name
            geometry = LineString(
                [input_intersection.geometry, output_intersection.geometry]
            )
            self.map_.add_link(
                Road(name, geometry, input_intersection, output_intersection, number_of_lanes=1)
            )
        self.map_.plot()
        self.map_.links.crs = "EPSG:4326"
        self.map_.intersections.crs = "EPSG:4326"
        self.map_.plot_folium(include_intersections=True)
        self.map_.to_geodigraph()


if __name__ == "__main__":
    unittest.main()
