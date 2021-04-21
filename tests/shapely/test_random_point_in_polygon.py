import unittest

from shapely.geometry import Polygon, box

from dpd.shapely import random_point_in_polygon


class Test_random_point_in_polygon(unittest.TestCase):
    def test_random_point_in_polygon(self):
        polygon = Polygon(box(0, 0, 10, 10))
        random_point_in_polygon(polygon)


if __name__ == "__main__":
    unittest.main()
