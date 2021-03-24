import unittest

from dpd.geometry import radius_of_curvature

p1 = [0, 0]
p2 = [1, 1]
p3 = [2, 3]


class TestRadiusOfCurvature(unittest.TestCase):
    def test_radius_of_curvature(self):
        self.assertEqual(radius_of_curvature(p1, p2, p3), 1.8263585701380227)


if __name__ == "__main__":
    unittest.main()
