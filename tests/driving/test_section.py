import unittest

from shapely.geometry import Point

from dpd.driving import Section


class TestSection(unittest.TestCase):
    def test_section(self):
        section = Section(Point(0, 0), Point(1, 0))
        self.assertEqual(section.speed_limit, None)
        self.assertEqual(section.geometry.length, 1.0)


if __name__ == "__main__":
    unittest.main()
