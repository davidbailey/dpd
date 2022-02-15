import unittest

from shapely.geometry import Point

from dpd.driving import StraightSection


class TestStraightSection(unittest.TestCase):
    def test_straight_section(self):
        straight_section = StraightSection(Point(0,0), Point(1,0))
        self.assertEqual(straight_section.speed_limit, None)
        self.assertEqual(straight_section.geometry.length, 1.0)


if __name__ == "__main__":
    unittest.main()
