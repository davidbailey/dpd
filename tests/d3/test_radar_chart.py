import unittest

from dpd.d3 import radar_chart


class TestRadarChart(unittest.TestCase):
    def test_radar_chart(self):
        self.assertIsNotNone(radar_chart(["test"], [], "test title"))


if __name__ == "__main__":
    unittest.main()
