import unittest

from shapely.geometry import LineString

from dpd.shapely import cut

line = LineString([(1, 2), (2, 4), (4, 5)])
length = 2


class TestCut(unittest.TestCase):
    def test_cut(self):
        self.a, self.b = cut(line, length)
        self.assertAlmostEqual(self.a.length, length)


if __name__ == "__main__":
    unittest.main()
