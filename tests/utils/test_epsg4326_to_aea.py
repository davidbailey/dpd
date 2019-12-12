import unittest

from shapely.geometry import Point

from dpd.utils import epsg4326_to_aea

class TestEPSG4326_To_AEA(unittest.TestCase):
    def test_epsg4326_to_aea(self):
        point = Point(-118.481389, 34.021944)
        aea_point = epsg4326_to_aea(point)
        self.assertEqual(aea_point.x, -8258079.413088454)
        self.assertEqual(aea_point.y, 9514122.322348474)

if __name__ == '__main__':
    unittest.main()
