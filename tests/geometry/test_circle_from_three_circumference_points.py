import unittest

from dpd.geometry import circle_from_three_circumference_points


class TestCircleFromThreeCircumferencePoints(unittest.TestCase):
    def test_circle_from_three_circumference_points(self):
        self.assertEqual(
            circle_from_three_circumference_points((1, 0), (-1, 0), (0, 1)),
            ((0.0, -0.0), 1.0),
        )
        self.assertEqual(
            circle_from_three_circumference_points((1, -6), (2, 1), (5, 2)),
            ((5.0, -3.0), 5.0),
        )


if __name__ == "__main__":
    unittest.main()
