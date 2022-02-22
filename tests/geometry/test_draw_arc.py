from math import pi
import unittest

from shapely.geometry import LineString, Point

from dpd.geometry import draw_arc

radius = 10

start_point = Point(0, radius)
end_point = Point(radius, 0)


class TestDrawArc(unittest.TestCase):
    def test_draw_arc(self):
        arc = draw_arc(
            (start_point.x, start_point.y),
            (end_point.x, end_point.y),
            radius=radius,
            right_handed=True,
            number_of_points=16,
        )
        linestring = LineString(arc)
        self.assertAlmostEqual(linestring.length, pi * 2 * radius / 4)


if __name__ == "__main__":
    unittest.main()
