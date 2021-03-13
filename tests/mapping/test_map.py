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
            self.map_.add_road(
                Road(name, geometry, input_intersection, output_intersection, 1)
            )


if __name__ == "__main__":
    unittest.main()
