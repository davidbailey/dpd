import unittest

from shapely.geometry import Point

from dpd.utils import epsg4326_to_aea


class TestEPSG4326_To_AEA(unittest.TestCase):
    def test_epsg4326_to_aea(self):
        point = Point(-118.481389, 34.021944)
        aea_point = epsg4326_to_aea(point)
        self.assertEqual(aea_point.x, -1955052.147737653)
        self.assertEqual(aea_point.y, -468997.4237058063)


if __name__ == "__main__":
    unittest.main()
