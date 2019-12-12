import unittest

from shapely.geometry import Point

from dpd.utils import epsg4326_to_aea

class TestEPSG4326_To_AEA(unittest.TestCase):
    def test_epsg4326_to_aea(self):
        point = Point(1,1)
        aea_point = epsg4326_to_aea(point)
        self.assertEqual(aea_point.x, 128294.42841956337)
        self.assertEqual(aea_point.y, 96237.9213969674)

if __name__ == '__main__':
    unittest.main()
